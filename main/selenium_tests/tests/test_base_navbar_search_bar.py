from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from . import constants
import helpers


class TestSearchBarToDirectory(helpers.SeleniumTestCase):
    """Test suite for the usage of the search bar that land to directory.

    In https://github.com/cgstudiomap/cgstudiomap/issues/748, we started to implement
    a new search bar that is present in all the pages.

    The test suite tries to cover it features and make sure a search can be done
    in all pages.

    :Warning:
    This is experimental and conditional on the environment:
    To work for now, a local instance running, and only one database should be
    operational, or the tests will fall to the database selector.
    """

    def test_whenAStudioIsSearchedFromTheHomepage_thenDirectoryPageIsLoaded(self):
        """
        Given the homepage is opened
        When a studio is searched
        Then the page of the map listing is opened.
        """
        self._test_searchThroughSearchBar('/')

    def test_whenAStudioIsSearchedFromTheAboutPage_thenDirectoryPageIsLoaded(self):
        """
        Given the about page is opened
        When a studio is searched
        Then the page of the map listing is opened.
        """
        self._test_searchThroughSearchBar('/aboutus')

    def test_whenAStudioIsSearchedFromTheDirectoryPage_thenDirectortPageIsLoaded(self):
        """
        Given the directory page is opened
        When a studio is searched
        Then the page of the map listing is opened.
        """
        self._test_searchThroughSearchBar('/directory')

    def test_whenAStudioIsSearchedFromAStudioPage_thenDirectortPageIsLoaded(self):
        """
        Given a studio page is opened (CGStudioMap Page here)
        When a studio is searched
        Then the page of the map listing is opened.
        """
        self._test_searchThroughSearchBar('/directory/company/cg-studio-map-1')

    def _test_searchThroughSearchBar(self, url):
        """Perform the search from the search bar and check we end up in the
        directory page.
        """
        driver = self.driver
        driver.get(self.url_template.format(url))
        self.assertIn(constants.titles[url], driver.title)
        search_bar = driver.find_element_by_xpath(
            '//*[@id="home"]/nav/div/div[1]/ul/li/form/div/div/input[1]'
        )
        search_bar.send_keys('cgstudiomap')
        search_bar.send_keys(Keys.RETURN)
        # Wait for the page to be loaded. Otherwise we might test for the
        # previous page actually.
        WebDriverWait(driver, self.delay).until(
            EC.presence_of_element_located((By.ID, 'footer_map'))
        )
        self.assertEqual(constants.titles['/directory'], driver.title)


class TestNavBarLinks(helpers.SeleniumTestCase):
    """Test suite for the links of the navbar."""

    def test_whenClickOnAboutLink_thenThePageAboutusIsLoaded(self):
        """
        Given the homepage is opened
        When the user click on the About link
        Then the page aboutus is opened
        """
        self.driver.get(self.url_template.format('/'))
        about_element = self.driver.find_element_by_xpath(
            '//*[@id="home"]/nav/div/div[2]/ul[1]/li[1]/a'
        )
        self.driver.get(about_element.get_attribute('href'))

        WebDriverWait(self.driver, self.delay).until(
            EC.presence_of_element_located((By.ID, 'aboutus'))
        )
        self.assertEqual(constants.titles['/aboutus'], self.driver.title)

    def test_whenClickOnTheIconOfTheNavbar_thenTheHomepageIsLoaded(self):
        """
        Given the about page is opened
        When the user click on the icon on the navbar
        Then the home page is opened
        """
        self.driver.get(self.url_template.format('/aboutus'))
        element = self.driver.find_element_by_xpath(
            '//*[@id="home"]/nav/div/div[1]/span/a'
        )
        self.driver.get(element.get_attribute('href'))

        WebDriverWait(self.driver, self.delay).until(
            EC.presence_of_element_located((By.ID, 'geochart_target'))
        )
        self.assertEqual(constants.titles['/'], self.driver.title)

    def test_whenClickOnContributeLink_thenCgstudiomapGithubPage(self):
        """
        Given the homepage is opened
        When the user click on the Contribute link
        Then the github page of cgstudiomap is opened
        """
        self.driver.get(self.url_template.format('/'))
        contribute_element = self.driver.find_element_by_xpath(
            '//*[@id="home"]/nav/div/div[2]/ul[1]/li[2]/a'
        )
        self.driver.get(contribute_element.get_attribute('href'))

        WebDriverWait(self.driver, self.delay).until(
            EC.presence_of_element_located((By.ID, 'facebox'))
        )
        self.assertEqual('GitHub - cgstudiomap/cgstudiomap', self.driver.title)


class TestFooterHomePage(helpers.SeleniumChromeTestCase):
    """Test suite for the footer of the homepage."""

    def test_whenDirectoryLinkIsClicked_thenThePageDirectoryIsOpened(self):
        """
        Given the user is on the homepage
        When he clicks the "directory" link
        Then the page directory (map) is opened
        """
        self.assertTrue(False)

    def test_whenAboutLinkIsClicked_thenTheAboutPageIsOpened(self):
        """
        Given the user is on the homepage
        When he clicks the "About" link
        Then the page About is opened
        """
        self.assertTrue(False)

    def test_whenContributeLinkIsClicked_thenTheGithubPageIsOpened(self):
        """
        Given the user is on the homepage
        When he clicks the "Contribute" link
        Then the github page of cgstudiomap is opened
        """
        self.assertTrue(False)

    def test_whenTheTwitterIconIsClicked_thenOurTwitterPageIsOpened(self):
        """
        Given the user is on the homepage
        When he clicks the "Twitter" icon
        Then the twitter page of cgstudiomap is opened
        """
        self.assertTrue(False)

    def test_whenTheLinkedinIconIsClicked_thenOurLinkedinPageIsOpened(self):
        """
        Given the user is on the homepage
        When he clicks the "Linkedin" icon
        Then the linkedin page of cgstudiomap is opened
        """
        self.assertTrue(False)

    def test_whenTheGithubIconIsClicked_thenOurGithubPageIsOpened(self):
        """
        Given the user is on the homepage
        When he clicks the "Github" icon
        Then the Github page of cgstudiomap is opened
        """
        self.assertTrue(False)
