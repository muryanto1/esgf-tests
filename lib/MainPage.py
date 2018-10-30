import time

from BasePage import BasePage
from BasePage import InvalidPageException
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MainPage(BasePage):

    _home_locator = "//div[@id='top_nav_left']//a[contains(text(), 'Home')]"
    _login_page_locator = "//a[contains(text(),'Login')]"

    def __init__(self, driver):
        super(MainPage, self).__init__(driver)

    def _validate_page(self, driver):
        # validate Main page is displaying a 'Home' tab
        home_tab_element = driver.find_element_by_xpath(self._home_locator)

    def goto_login_page(self):
        login_page_element = self.driver.find_element_by_xpath(self._login_page_locator)
        login_page_element.click()

    
