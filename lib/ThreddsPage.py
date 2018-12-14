import time

from BasePage import BasePage
from BasePage import InvalidPageException
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from LoginPage import DataAccessLoginPage

class ThreddsPage(BasePage):

    # old thredds
    #_root_catalog_locator = "//a//tt[contains(text(), 'Earth System Root catalog')]"
    #_test_folder_locator = "//tt[contains(text(), 'test')]"
    #_test_file_locator = "//tt[contains(text(), 'nc')]"

    _root_catalog_locator = "//a//code[contains(text(), 'Earth System Root catalog')]"
    _test_folder_locator = "//code[contains(text(), 'test')]"
    _test_file_locator = "//code[contains(text(), 'nc')]"

    _download_li_locator = "//tr//td//a"

    # old thredds has : at the end of each text
    download_map = {"http": "HTTPServer",
                     "ftp": "GridFTP",
                     "dap": "OpenDAP"}

    def __init__(self, driver, server):
        super(ThreddsPage, self).__init__(driver, server)

    def _validate_page(self):
        print("xxx ThreddsPage _validate_page()")
        self.load_page(self.get_idp_server(), 'thredds')
        try:
            root_catalog_element  = self.driver.find_element_by_xpath(self._root_catalog_locator)
        except NoSuchElementException:
            raise InvalidPageException

        if self.get_idp_server() is None:
            self.set_idp_server()
        print("xxx ThreddsPage _validate_page() is good")

    def _go_through_catalog(self):
        print("xxx click on root_catalog xxx")
        self.driver.find_element_by_xpath(self._root_catalog_locator).click()

        print("xxx click on test_folder xxx")
        self.driver.find_element_by_xpath(self._test_folder_locator).click()

        print("xxx click on test_file_locator xxx")
        file_name = self.driver.find_element_by_xpath(self._test_file_locator).text
        self.driver.find_element_by_xpath(self._test_file_locator).click()

        print("...file to be download: {f}".format(f=file_name))
        return file_name

    def _select_download_type(self, type):
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
        # TEMPORARY
        ext_open_id = "https://esgf-node.llnl.gov/esgf-idp/openid/"
        data_access_login_page._select_open_id_from_drop_down(ext_open_id)

    def __select_li_for_download_type(self, file_name, type):
        # for http
        _path_locator = "/thredds/fileServer/esg_dataroot/test/{f}".format(f=file_name)
        _download_file_locator = "//a[@href=\"{f}\"]".format(f=_path_locator)

        print("...find the link to click for {t} download".format(t=type))
        li_elements = self.driver.find_elements_by_xpath(self._download_li_locator)
        for element in li_elements:
            print("....going through each element....")
            download_type = element.find_element_by_xpath(".//b").text
            print("xxx DEBUG...download_type: {d}, text: {t}".format(d=download_type,
                                                                     t=self.download_map[type]))
            if download_type == self.download_map[type]:
                print("...found the element to click for {t} download".format(t=type))
                time.sleep(self._delay)
                print("...click on the link for {t} download".format(t=type))
                #self.driver.find_element_by_xpath(_download_file_locator).click()
                #wait = WebDriverWait(self.driver, 10)
                #el = wait.until(EC.element_to_be_clickable((By.XPATH, _download_file_locator)))
                #download = self.driver.find_element_by_xpath(_download_file_locator)
                #download.click()

                #wait = WebDriverWait(self.driver, 10)
                #download = self.driver.find_element_by_xpath(_download_file_locator)
                #actionChains = ActionChains(self.driver)
                #actionChains.move_to_element(download).perform()
                #clickable_el = wait.until(EC.element_to_be_clickable((By.XPATH, _download_file_locator)))
                #clickable_el.click()

                download_el = self.driver.find_element_by_xpath(_download_file_locator)
                self.driver.execute_script("arguments[0].click();", download_el)
                time.sleep(self._delay)
                break
