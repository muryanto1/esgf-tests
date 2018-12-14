import time

from BasePage import BasePage
from BasePage import InvalidPageException
from LoginPage import LoginPage
from LoginPage import OpenIDLoginPage

from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MainPage(BasePage):

    _home_locator = "//div[@id='top_nav_left']//a[contains(text(), 'Home')]"
    _login_page_locator = "//a[contains(text(),'Login')]"
    _logout_locator = "//a[contains(text(),'Log out')]"

    def __init__(self, driver, idp_server):
        super(MainPage, self).__init__(driver, idp_server)
        
    def _validate_page(self):
        # validate Main page is displaying a 'Home' tab
        print("xxx MainPage _validate_page xxx")
        home_tab_element = self.driver.find_element_by_xpath(self._home_locator)
        print("xxx MainPage _validate_page is good xxx")

    def _goto_login_page(self):
        login_page_element = self.driver.find_element_by_xpath(self._login_page_locator)
        login_page_element.click()


    def do_login(self, user, password):
        idp_server = self.get_idp_server()
        self._goto_login_page()
        login_page = LoginPage(self.driver, idp_server)
        login_page._login(idp_server, user, password)
        openIdLoginPage = OpenIDLoginPage(self.driver, idp_server)
        openIdLoginPage._enter_credentials(user, password)
    
    def do_logout(self):
        logout_element = self.driver.find_element_by_xpath(self._logout_locator)
        logout_element.click()
