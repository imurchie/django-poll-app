import unittest
from selenium import webdriver

from helpers import on_platforms

# browsers = [{
#                 "platform": "MAC",
#                 "browserName": "chrome",
#                 "version": "38"
#             }]

browsers = [{
                "platform": "MAC",
                "browserName": "safari",
                "version": "7"
            }]


@on_platforms(browsers)
class TestPollSelenium(unittest.TestCase):
    def setUp(self):
        command_executor = 'http://localhost:4444/wd/hub'
        self.driver = webdriver.Remote(
            desired_capabilities=self.desired_capabilities,
            command_executor=command_executor
        )
        self.driver.implicitly_wait(30)

    def tearDown(self):
        self.driver.quit()

    def test_poll_index(self):
        self.driver.get('http://localhost:8000/polls/')
        assert 'Poll Index' in self.driver.title

        el = self.driver.find_element_by_link_text('What\'s up?')
        assert el != None

    def test_poll_detail(self):
        self.driver.get('http://localhost:8000/polls/')
        self.driver.find_element_by_link_text('What\'s up?').click()
        assert 'Poll: What\'s up?' in self.driver.title

    def test_poll_vote(self):
        self.driver.get('http://localhost:8000/polls/1/')

        self.driver.find_element_by_css_selector("input[type='submit']").click()

        assert 'You didn\'t select a choice.' in self.driver.page_source

        self.driver.find_element_by_css_selector("input[type='radio']").click()

        # need to re-find, since it is a full request/reload, not ajax
        self.driver.find_element_by_css_selector("input[type='submit']").click()

        assert 'http://localhost:8000/polls/1/results/' == self.driver.current_url
