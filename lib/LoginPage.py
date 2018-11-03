import time

from BasePage import BasePage
from BasePage import InvalidPageException
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage(BasePage):

    _openID_heading_locator = "//h2[contains(text(), 'OpenID Login')]"
    # input text area for openid
    _openid_locator = "openid_identifier"
    # login button
    _openid_login_locator = "//input[@value='Login']"

    def __init__(self, driver, idp_server):
        super(LoginPage, self).__init__(driver, idp_server)

    def _validate_page(self, driver):
        # validate Login Page is displaying 'OpenID Login'
        print("xxx LoginPage._validate_page()")
        open_id_header = driver.find_element_by_xpath(self._openID_heading_locator)

    def _login(self, idp_server, user, password):
        open_id = "https://{s}/esgf-idp/openid/{u}".format(s=idp_server,
                                                           u=user)
        print("xxx open_id: {o}".format(o=open_id))
        self.driver.find_element_by_id(self._openid_locator).send_keys(open_id)
        time.sleep(4)
        self.driver.find_element_by_xpath(self._openid_login_locator).click()
        time.sleep(4)

        
class OpenIDLoginPage(BasePage):
    '''
    This is for ESGF OpenID Login page -- which is the page we get to after
    we enter an open id in the LoginPage
    i.e.: https://<node>.llnl.gov/esgf-idp/idp/login.htm
    '''
    _esgf_open_id_heading_locator = "//h1[contains(text(), 'ESGF OpenID Login')]"
    # user name and password text input area
    _esgf_open_id_username_locator = "username"
    _esgf_open_id_password_locator = "password"
    _submit_locator = "//input[@class='button' and @value='SUBMIT']"

    def __init__(self, driver, idp_server):
        super(OpenIDLoginPage, self).__init__(driver, idp_server)

    def _validate_page(self, driver):
        # validate page displaying 'ESGF OpenID Login'
        print("xxx OpenIDLoginPage._validate_page()")
        esgf_open_id_header = driver.find_element_by_xpath(self._esgf_open_id_heading_locator)
    
    def _enter_credentials(self, username, password):
        print("xxx _enter_credentials xxx")
        self.driver.find_element_by_id(self._esgf_open_id_username_locator).send_keys(username)
        self.driver.find_element_by_id(self._esgf_open_id_password_locator).send_keys(password)
        time.sleep(2)
        self.driver.find_element_by_xpath(self._submit_locator).click()
        time.sleep(4)


        


