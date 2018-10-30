import os
import sys
import time
import unittest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pytest_testconfig import config

# NEED pytest-testconfig
this_dir = os.path.abspath(os.path.dirname(__file__))
lib_dir = os.path.join(this_dir, '..', 'lib')
sys.path.append(lib_dir)

from TestConfig import *

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
        #self.driver = webdriver.Firefox(firefox_options=options, executable_path="/usr/local/bin/geckodriver")
        self.driver.implicitly_wait(10)
        idp_server = self._get_idp_server()
        self.driver.get("https://{n}".format(n=idp_server))
        time.sleep(3)

    def _get_test_user_credentials(self):
        user = config[ACCOUNT_SECTION][USER_NAME_KEY]
        password = config[ACCOUNT_SECTION][USER_PASSWORD_KEY]
        return(user, password)

    def _get_idp_server(self):
        idp_server = config[NODES_SECTION][IDP_NODE_KEY]
        return(idp_server)

    def tearDown(self):
        self.driver.quit()
