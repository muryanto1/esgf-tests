import requests

from abc import abstractmethod

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

class BasePage(object):
    """ All page objects inherit from this """

    _wait_timeout = 10
    _delay = 3

    def __init__(self, driver, idp_server):
        self._validate_page(driver)
        self.driver = driver
        self._idp_server = idp_server

    @abstractmethod
    def _validate_page(self, driver):
        return

    def load_page(self, url, expected_element=(By.TAG_NAME, 'html'), 
                  timeout=_wait_timeout):
        try:
            r = requests.get(url, verify=False, timeout=timeout)
            err_msg = "fail to connect to '{0}' (code = {1})".format(url, r.status_code)
            assert(r.status_code < 403), err_msg
        except Exception as e:
            err_msg = "fail to connect to '{0}' (reason: {1})".format(url, e)
            assert(False), err_msg

        try:
            self.driver.get(url)
        except TimeoutException:
            assert(False), "page not found or timeout for {0}".format(url)

        element = expected_conditions.presence_of_element_located(expected_element)
        try:
            WebDriverWait(self.driver, timeout).until(element)
        except TimeoutException:
            assert(False), "page not found or timeout  for {0}".format(url)

    def get_idp_server(self):
        return(self._idp_server)

class InvalidPageException(Exception):
    """ Throw this exception when we do not find the correct page """
    pass

