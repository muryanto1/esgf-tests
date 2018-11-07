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

class ThreddsPage(BasePage):

    _root_catalog_locator = "//a//tt[contains(text(), 'Earth System Root catalog')]"
    _test_folder_locator = "//tt[contains(text(), 'test')]"
    _test_file_locator = "//tt[contains(text(), 'nc')]"

    _download_li_locator = "//ol//li"

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

    def _go_through_catalog(self):
        self.driver.find_element_by_xpath(self._root_catalog_locator).click()        
        self.driver.find_element_by_xpath(self._test_folder_locator).click()
        file_name = self.driver.find_element_by_xpath(self._test_file_locator).text
        self.driver.find_element_by_xpath(self._test_file_locator).click()

        print("...file to be download: {f}".format(f=file_name))
        return file_name

    def _select_download_type(self, type,
                              username=None, password=None):
        file_name = self._go_through_catalog()
        idp_server = self.get_idp_server()

        self.__select_li_for_download_type(file_name, type)
        return file_name

    def _do_download_external_idp_authentication(self, type,
                                                 username=None, password=None):

        file_name = self._go_through_catalog()
        idp_server = self.get_idp_server()
        self.__select_li_for_download_type(file_name, type)
        try:
            data_access_login_page = DataAccessLoginPage(self.driver,
                                                         idp_server)
        except InvalidPageException:
            print("Not getting the expected DataAccessLoginPage")

        # click on the arrow to get the drop down
        data_access_login_page._select_open_id_from_drop_down()

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
