import time

from BasePage import BasePage
from BasePage import InvalidPageException
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver import ActionChains

class LoginPage(BasePage):

    _openID_heading_locator = "//h2[contains(text(), 'OpenID Login')]"
    # input text area for openid
    _openid_locator = "openid_identifier"
    # login button
    _openid_login_locator = "//input[@value='Login']"

    def __init__(self, driver, idp_server):
        super(LoginPage, self).__init__(driver, idp_server)

    def _validate_page(self):
        # validate Login Page is displaying 'OpenID Login'
        print("...LoginPage._validate_page()")
        open_id_header = self.driver.find_element_by_xpath(self._openID_heading_locator)

    def _login(self, idp_server, user, password):
        open_id = "https://{s}/esgf-idp/openid/{u}".format(s=idp_server,
                                                           u=user)
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

    def _validate_page(self):
        # validate page displaying 'ESGF OpenID Login'
        print("...OpenIDLoginPage._validate_page()")
        esgf_open_id_header = self.driver.find_element_by_xpath(self._esgf_open_id_heading_locator)
    
    def _enter_credentials(self, username, password):
        print("...OpenIdLoginPage._enter_credentials()...")
        self.driver.find_element_by_id(self._esgf_open_id_username_locator).send_keys(username)
        self.driver.find_element_by_id(self._esgf_open_id_password_locator).send_keys(password)
        time.sleep(2)
        self.driver.find_element_by_xpath(self._submit_locator).click()
        time.sleep(4)

    def _enter_password(self, password):
        print("...OpenIdLoginPage._enter_password()...")
        self.driver.find_element_by_id(self._esgf_open_id_password_locator).send_keys(password)
        time.sleep(2)
        self.driver.find_element_by_xpath(self._submit_locator).click()
        time.sleep(4)

class DataAccessLoginPage(BasePage):
    '''
    This is for 'Data Access Login' page - esg_orp
    '''
    _data_access_login_heading_locator = "//h1[contains(text(), 'Data Access Login')]"
    _drop_down_arrow_locator = "//a[@title='Show All Items']"
    _open_id_input_locator = "//span[@class='custom-combobox']//input[@class='custom-combobox-input ui-widget ui-widget-content ui-state-default ui-corner-left ui-autocomplete-input']"
    _open_id_go_locator = "//input[@value='GO']"

    _drop_down_locator = "//select[@name='openid_identifier']"

    def __init__(self, driver, server):
        super(DataAccessLoginPage, self).__init__(driver, server)
        #self.load_page(server)

    def _validate_page(self):
        # validate page displaying 'Data Access Login':
        print("...DataAccessLoginPage._validate_page()...")
        try:
            self.driver.find_element_by_xpath(self._data_access_login_heading_locator)    
        except NoSuchElementException:
            raise InvalidPageException
        if self.get_idp_server() is None:
            self.set_idp_server()

    def _enter_open_id(self, idp_server, username):
        print("...DataAccessLoginPage._enter_open_id()...")
        open_id = "https://{s}/esgf-idp/openid/{u}".format(s=idp_server,
                                                           u=username)
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





        

