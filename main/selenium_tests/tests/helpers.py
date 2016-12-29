import os
import unittest
from selenium import webdriver


class SeleniumTestCase(unittest.TestCase):
    """Helper to setup a common environment for selenium tests."""
    url_template = 'http://localhost:8069{}'
    phantomjs_path = os.path.join(
        os.path.dirname(__file__),
        '..', 'static', 'src', 'js', 'phantomjs', 'bin', 'phantomjs'
    )
    delay = 3  # seconds

    def setUp(self):
        """Give a driver."""
        self.set_driver()

    def tearDown(self):
        """Close the driver"""
        self.driver.close()

    def set_driver(self):
        """set :attr:`driver`."""
        self.driver = webdriver.PhantomJS(executable_path=self.phantomjs_path)

class SeleniumChromeTestCase(SeleniumTestCase):
    def set_driver(self):
        self.driver = webdriver.Chrome()

class SeleniumFirefoxTestCase(SeleniumTestCase):
    def set_driver(self):
        self.driver = webdriver.Firefox()
