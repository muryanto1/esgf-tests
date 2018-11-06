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
from ThreddsPage import ThreddsPage

from pytest_testconfig import config

class DownloadTest(BaseTestCase):

    _group_registration_request_locator = "//h1[contains(text(), 'Group Registration Request')]"
    def test_http_download_user_has_no_access(self):
        '''
        Test restricted access, have the following in esgf_policies_common.xml:
        <policy resource=".*test.*" attribute_type="wheel" attribute_value="super" action="Read"/>

        download data as test user and expect 'Group Registration Request' message
        '''
        idp_server = self._get_idp_server()
        main_page = MainPage(self.driver, idp_server)
        user, password = self._get_test_user_credentials()

        print("...loading thredds page...")
        main_page.load_page(idp_server, "thredds")
        time.sleep(10)
        thredds_page = ThreddsPage(self.driver, idp_server)

        download_dir = self._get_download_dir()
        file_name = thredds_page._do_download_restricted_access('http', user, password)
        assert self.driver.find_element_by_xpath(self._group_registration_request_locator)
        
        time.sleep(5)

    def test_http_download_user_as_rootAdmin(self):
        '''
        Test restricted access, have the following in esgf_policies_common.xml:
        <policy resource=".*test.*" attribute_type="wheel" attribute_value="super" action="Read"/>

        download data as test user and expect 'Group Registration Request' message
        '''
        idp_server = self._get_idp_server()
        main_page = MainPage(self.driver, idp_server)
        #user, password = self._get_test_user_credentials()
        # REVISIT
        user = 'rootAdmin'
        password = 'EsgfLLNL'

        #main_page.do_login(idp_server, user, password)
        #urllib3.disable_warnings()
        main_page.load_page(idp_server, "thredds")
        time.sleep(10)
        thredds_page = ThreddsPage(self.driver, idp_server)
        download_dir = self._get_download_dir()
        file_name = thredds_page._do_download_restricted_access('http', user, password)
        assert os.path.isfile(os.path.join(download_dir, file_name))
        time.sleep(5)

    def ABCtest_http_download_login_first(self):
        # get info from test config                                                                                 
        user, password = self._get_test_user_credentials()
        idp_server = self._get_idp_server()
        main_page = MainPage(self.driver, idp_server)

        # main_page.load_page(idp_server)
        main_page.do_login(user, password)
        print("xxx...test_http_download_login_first(), idp_server: {s}".format(s=idp_server))
        time.sleep(10)

        thredds_page = ThreddsPage(self.driver, idp_server)
        print("xxx after instantiating thredds_page...")

        download_dir = self._get_download_dir()
        file_name = thredds_page._do_download('http')
        print("xxx xxx test_http_download: dir: {d}, filename: {f}".format(d=download_dir,
                                                                           f=file_name))
        time.sleep(2)
        assert os.path.isfile(os.path.join(download_dir, file_name))

if __name__ == '__main__':
    unittest.main(verbosity=2)

