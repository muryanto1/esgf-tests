import unittest
import os 
import sys
import time

this_dir = os.path.abspath(os.path.dirname(__file__))
lib_dir = os.path.join(this_dir, '..', 'lib')
sys.path.append(lib_dir)

# from BaseTestCase import BaseTestCase
from BaseTestCase import BaseTestCase
from MainPage import MainPage
from LoginPage import LoginPage
from LoginPage import OpenIDLoginPage
from pytest_testconfig import config

class LoginTest(BaseTestCase):

    def test_root_login(self):
        main_page = MainPage(self.driver)
        main_page.goto_login_page()
        print("hello....")

        login_page = LoginPage(self.driver)
        
        user, password = self._get_test_user_credentials()
        print("xxx user: {u}, passwd: {p}".format(u=user, p=password))
        idp_server = self._get_idp_server()
        print("xxx idp_server: {s}".format(s=idp_server))
        login_page._login(idp_server, user, password)

        openIdLoginPage = OpenIDLoginPage(self.driver)
        openIdLoginPage._enter_credentials(user, password)

if __name__ == '__main__':
    unittest.main(verbosity=2)

