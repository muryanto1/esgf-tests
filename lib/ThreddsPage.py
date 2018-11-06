import time

from BasePage import BasePage
from BasePage import InvalidPageException
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from LoginPage import DataAccessLoginPage
from LoginPage import OpenIDLoginPage

class ThreddsPage(BasePage):

    _root_catalog_locator = "//a//tt[contains(text(), 'Earth System Root catalog')]"
    _test_folder_locator = "//tt[contains(text(), 'test')]"
    _test_file_locator = "//tt[contains(text(), 'nc')]"

    _download_li_locator = "//ol//li"

    _open_id_input_locator = "//span[@class='custom-combobox']//input[@class='custom-combobox-input ui-widget ui-widget-content ui-state-default ui-corner-left ui-autocomplete-input']"
    _open_id_go_locator = "//input[@value='GO']"

    download_map = {"http": "HTTPServer:",
                     "ftp": "GridFTP:",
                     "dap": "OpenDAP:"}

    def __init__(self, driver, server):
        super(ThreddsPage, self).__init__(driver, server)

    def _validate_page(self):
        self.load_page(self.get_idp_server(), 'thredds')
        try:
            root_catalog_element  = self.driver.find_element_by_xpath(self._root_catalog_locator)
        except NoSuchElementException:
            raise InvalidPageException

        if self.get_idp_server() is None:
            self.set_idp_server()

    def _do_download(self, type, username=None, password=None):
        # starting from thredds top level page, and user not logged in
        self.driver.find_element_by_xpath(self._root_catalog_locator).click()        
        self.driver.find_element_by_xpath(self._test_folder_locator).click()
        file_name = self.driver.find_element_by_xpath(self._test_file_locator).text
        print("xxx xxx file to be download: {f}".format(f=file_name))
        idp_server = self.get_idp_server()

        self.driver.find_element_by_xpath(self._test_file_locator).click()
        self.__select_li_for_download_type(file_name, type)

        try:
            print("xxx DEBUG...idp_server: {s}".format(s=idp_server))
            data_access_login_page = DataAccessLoginPage(self.driver,
                                                         idp_server)
        except InvalidPageException:
            print("Not getting the expected DataAccessLoginPage")
       
        open_id = "https://{s}/esgf-idp/openid/{u}".format(s=self.get_idp_server(),
                                                           u=username)
        print("xxx open_id: {i}".format(i=open_id))
        try:
            self.driver.find_element_by_xpath(self._open_id_input_locator)
        except NoSuchElementException:
            print("FAIL...did not find the OpenID drop down")
            raise NoSuchElementException

        self.driver.find_element_by_xpath(self._open_id_input_locator).send_keys(open_id)
        time.sleep(3)
        self.driver.find_element_by_xpath(self._open_id_go_locator).click()
        time.sleep(5)
        openIdLoginPage = OpenIDLoginPage(self.driver, idp_server)
        openIdLoginPage._enter_password(password)

        return file_name

    def _do_download_restricted_access(self, type,
                                       username=None, password=None):
        # starting from thredds top level page, and user not logged in

        self.driver.find_element_by_xpath(self._root_catalog_locator).click()        
        self.driver.find_element_by_xpath(self._test_folder_locator).click()
        file_name = self.driver.find_element_by_xpath(self._test_file_locator).text
        print("...file to be download: {f}".format(f=file_name))
        idp_server = self.get_idp_server()

        self.driver.find_element_by_xpath(self._test_file_locator).click()
        self.__select_li_for_download_type(file_name, type)

        try:
            data_access_login_page = DataAccessLoginPage(self.driver,
                                                         idp_server)
        except InvalidPageException:
            print("Not getting the expected DataAccessLoginPage")
       
        open_id = "https://{s}/esgf-idp/openid/{u}".format(s=self.get_idp_server(),
                                                           u=username)
        print("...open_id: {i}".format(i=open_id))
        try:
            open_id_input_el = self.driver.find_element_by_xpath(self._open_id_input_locator)
        except NoSuchElementException:
            print("FAIL...did not find the OpenID input area")
            raise NoSuchElementException

        open_id_input_el.send_keys(open_id)
        time.sleep(self._delay)
        print("...click on 'GO' button")
        self.driver.find_element_by_xpath(self._open_id_go_locator).click()
        time.sleep(self._delay)

        try:
            openIdLoginPage = OpenIDLoginPage(self.driver, idp_server)
            openIdLoginPage._enter_password(password)
        except InvalidPageException:
            print("Not getting the expected OpenIdLoginPage")
            raise InvalidPageException

        #if user_has_access is False:
        #    try:
        #        self.driver.find_element_by_xpath(self._group_registration_request_locator)
        #        return None
        #    except NoSuchElementException:
        #        print("Fail...should be getting a 'Group Registration Request'")
        #        raise NoSuchElementException    
        return file_name

    def __select_li_for_download_type(self, file_name, type):
        _path_locator = "/thredds/fileServer/esg_dataroot/test/{f}".format(f=file_name)
        _download_file_locator = ".//a[contains(text(), {f})]".format(f=_path_locator)

        print("...find the link to click for {t} download".format(t=type))
        li_elements = self.driver.find_elements_by_xpath(self._download_li_locator)
        for element in li_elements:
            download_type = element.find_element_by_xpath(".//b").text
            if download_type == self.download_map[type]:
                print("...found the element to click for {t} download".format(t=type))
                time.sleep(self._delay)
                print("...click on the link for {t} download".format(t=type))
                element.find_element_by_xpath(_download_file_locator).click()
                time.sleep(self._delay)
                break
