import unittest
import os 
import sys
import time

this_dir = os.path.abspath(os.path.dirname(__file__))
lib_dir = os.path.join(this_dir, '..', 'lib')
sys.path.append(lib_dir)

print("xxx xxx lib_dir: {d}".format(d=lib_dir))

# from BaseTestCase import BaseTestCase
from BaseTestCase import BaseTestCase
from MainPage import MainPage
# from LoginPage import LoginPage
# from LoginPage import OpenIDLoginPage
from pytest_testconfig import config

class LoginTest(BaseTestCase):

    def test_user_login(self):
        main_page = MainPage(self.driver)
        user, password = self._get_test_user_credentials()
        idp_server = self._get_idp_server()
        main_page.do_login(idp_server, user, password)
        # may need to REVISIT -- validate
        main_page.do_logout()
        print("xxx after do_logout()")
        time.sleep(4)

if __name__ == '__main__':
    unittest.main(verbosity=2)

