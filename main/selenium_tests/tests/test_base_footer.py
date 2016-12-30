"""
Test suite for the footer, as defined as the base for all pages.
================================================================
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from . import constants
import helpers


class TestFooterHomePage(helpers.SeleniumTestCase):
    """Test suite for the footer of the homepage."""

    def test_whenDirectoryLinkIsClicked_thenThePageDirectoryIsOpened(self):
        """
        Given the user is on the homepage
        When he clicks the "directory" link
        Then the page directory (map) is opened
        """
        self.assertTrue(False, msg="test in WIP")

    def test_whenAboutLinkIsClicked_thenTheAboutPageIsOpened(self):
        """
        Given the user is on the homepage
        When he clicks the "About" link
        Then the page About is opened
        """
        self.assertTrue(False, msg="test in WIP")

    def test_whenContributeLinkIsClicked_thenTheGithubPageIsOpened(self):
        """
        Given the user is on the homepage
        When he clicks the "Contribute" link
        Then the github page of cgstudiomap is opened
        """
        self.assertTrue(False, msg="test in WIP")

    def test_whenTheTwitterIconIsClicked_thenOurTwitterPageIsOpened(self):
        """
        Given the user is on the homepage
        When he clicks the "Twitter" icon
        Then the twitter page of cgstudiomap is opened
        """
        self.assertTrue(False, msg="test in WIP")

    def test_whenTheLinkedinIconIsClicked_thenOurLinkedinPageIsOpened(self):
        """
        Given the user is on the homepage
        When he clicks the "Linkedin" icon
        Then the linkedin page of cgstudiomap is opened
        """
        self.assertTrue(False, msg="test in WIP")

    def test_whenTheGithubIconIsClicked_thenOurGithubPageIsOpened(self):
        """
        Given the user is on the homepage
        When he clicks the "Github" icon
        Then the Github page of cgstudiomap is opened
        """
        self.assertTrue(False, msg="test in WIP")
