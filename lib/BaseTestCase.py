import os
import sys
import time
import unittest
import tempfile

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pytest_testconfig import config

from selenium.webdriver import DesiredCapabilities, Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# NEED pytest-testconfig
#this_dir = os.path.abspath(os.path.dirname(__file__))
#lib_dir = os.path.join(this_dir, '..', 'lib')
#sys.path.append(lib_dir)

from TestConfig import *

class BaseTestCase(unittest.TestCase):

    _delay = 3
    def setUp(self):        

        #_download_dir = "/tmp"
        self._download_dir = tempfile.mkdtemp()
        print("...download_dir: {d}".format(d=self._download_dir))
        browser = config[BROWSER_SECTION][BROWSER_KEY]
        options = Options()
        options.add_argument("--headless")
        #options.add_argument("--foreground")

        if browser == 'chrome':
            #options.binary_location = "/usr/local/bin/chromedriver"
            chrome_options = webdriver.ChromeOptions()
            #chrome_options.binary_location = "/usr/local/bin/chromedriver"
            ##chrome_options.add_argument("--headless")
            preferences = {"download.default_directory": self._download_dir,
                           "directory_upgrade": True,
                           "safebrowsing.enabled": True,
                           "prompt_for_download": "false"}
            chrome_options.add_experimental_option("prefs", preferences)
            self.driver = webdriver.Chrome(options=chrome_options)
        elif browser == 'firefox':
            firefox_profile = FirefoxProfile() # profile                                                                            
            firefox_profile.set_preference('extensions.logging.enabled', False)
            firefox_profile.set_preference('network.dns.disableIPv6', False)
            firefox_profile.set_preference('browser.download.dir', self._download_dir)
            firefox_profile.set_preference('browser.download.folderList', 2)
            firefox_profile.set_preference('browser.download.useDownloadDir', True)
            firefox_profile.set_preference('browser.download.panel.shown', False)
            firefox_profile.set_preference('browser.download.manager.showWhenStarting', False)
            firefox_profile.set_preference('browser.download.manager.showAlertOnComplete', False)
            
            firefox_capabilities = DesiredCapabilities().FIREFOX
            firefox_capabilities['marionette'] = True
            firefox_capabilities['moz:firefoxOptions'] = {'args': ['--headless']}

            options.binary_location = "/usr/local/bin/geckodriver"
            firefox_binary = FirefoxBinary("/opt/firefox58/firefox")        
            self.driver = webdriver.Firefox(firefox_profile=firefox_profile,
                                            firefox_binary=firefox_binary,
                                            options=options,
                                            capabilities = firefox_capabilities,
                                            executable_path="/usr/local/bin/geckodriver")

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

    def _get_download_dir(self):
        return self._download_dir

    def tearDown(self):
        self.driver.quit()
