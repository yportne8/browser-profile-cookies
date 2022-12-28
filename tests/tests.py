import unittest
from pathlib import WindowsPath
from http.cookiejar import CookieJar, Cookie

from browser import Profile



COOKIES = None # Set at if __name__.
DEFAULT = None # Set at if __name__.


class TestBrowser(unittest.TestCase):


    def test_browsers(self):
        browsers = COOKIES.browsers
        self.assertTrue(type(browsers) == dict)

    def test_profiles(self):
        profiles = COOKIES.profiles
        self.assertTrue(type(profiles) == dict)
    
    def test_browser(self):
        COOKIES.browser = "edge"
        browser = COOKIES.browser
        self.assertTrue(type(browser) == str)
    
    def test_path(self):
        self.assertTrue(type(COOKIES.path) == WindowsPath)

    def test_userdata(self):
        self.assertTrue(COOKIES.userdata)

    def test_localstate(self):
        self.assertTrue(COOKIES.localstate)

    def test_profile(self):
        COOKIES.profile = DEFAULT
        self.assertTrue(COOKIES.profile)
    
    def test_cookiejar(self):
        self.assertTrue(type(COOKIES.cookiejar())==CookieJar)

    def test_cookie(self):
        self.assertTrue(type(COOKIES.cookie("msn"))==CookieJar)

    def test_cookiestring(self):
        self.assertTrue(type(COOKIES.cookie_string("msn"))==str)


if __name__ == '__main__':
    
    DEFAULT = "Default"
    try:
        COOKIES = Profile("edge", DEFAULT)
    except:
        DEFAULT = "Profile 1"
        try:
            COOKIES = Profile("edge", DEFAULT)    
        except:
            print("FAILED: Failed to create Profile instance.")

    unittest.main()