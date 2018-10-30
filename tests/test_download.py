import unittest
import os 
import sys
import time

this_dir = os.path.abspath(os.path.dirname(__file__))
lib_dir = os.path.join(this_dir, '..', 'lib')
sys.path.append(lib_dir)

#print("xxx xxx lib_dir: {d}".format(d=lib_dir))

# from BaseTestCase import BaseTestCase
from BaseTestCase import BaseTestCase
from MainPage import MainPage
from LoginPage import LoginPage
from LoginPage import OpenIDLoginPage
from pytest_testconfig import config

import urllib3


class DownloadTest(BaseTestCase):

    def test_http_download(self):
        main_page = MainPage(self.driver)
        user, password = self._get_test_user_credentials()
        idp_server = self._get_idp_server()
        main_page.do_login(idp_server, user, password)
        urllib3.disable_warnings()
        main_page.load_page("https://esgf-dev1.llnl.gov/thredds")
        time.sleep(10)


if __name__ == '__main__':
    unittest.main(verbosity=2)

