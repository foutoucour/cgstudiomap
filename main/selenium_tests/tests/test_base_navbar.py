"""
Test suite for the navbar, defined as the base for all pages.
=============================================================
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from . import constants
import helpers


class TestNavBarLinks(helpers.SeleniumTestCase):
    """Test suite for the links of the navbar."""

    def test_whenClickOnAboutLink_thenThePageAboutusIsLoaded(self):
        """
        Given the homepage is opened
        When the user click on the About link
        Then the page aboutus is opened
        """
        xpath = '//*[@id="home"]/nav/div/div[2]/ul[1]/li[1]/a'
        self.check_link('/', xpath, 'aboutus', constants.titles['/aboutus'])

    def test_whenClickOnTheIconOfTheNavbar_thenTheHomepageIsLoaded(self):
        """
        Given the about page is opened
        When the user click on the icon on the navbar
        Then the home page is opened
        """
        xpath = '//*[@id="home"]/nav/div/div[1]/span/a'
        self.check_link('/aboutus', xpath, 'footer_map', constants.titles['/'])

    def test_whenClickOnContributeLink_thenCgstudiomapGithubPage(self):
        """
        Given the homepage is opened
        When the user click on the Contribute link
        Then the github page of cgstudiomap is opened
        """
        xpath = '//*[@id="home"]/nav/div/div[2]/ul[1]/li[2]/a'
        self.check_link('/', xpath, 'facebox', constants.titles['github'])

    def check_link(self, url, xpath, element_to_wait, title):
        """Helper to test for the links

        :param str url: url of the page to run the test from.
        :param str xpath: xpath to find the element with the link
        :param str element_to_wait: name of the element to wait for.
                                    It will be used as a wait marker.
        :param str title: title of the page that is supposed to be loaded
        """
        self.driver.get(self.url_template.format(url))
        contribute_element = self.driver.find_element_by_xpath(xpath)
        self.driver.get(contribute_element.get_attribute('href'))
        WebDriverWait(self.driver, self.delay).until(
            EC.presence_of_element_located((By.ID, element_to_wait))
        )
        self.assertEqual(title, self.driver.title)
