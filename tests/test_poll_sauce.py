import os
import sys
import unittest
import sauceclient
from selenium import webdriver
from sauceclient import SauceClient

from helpers import on_platforms


USERNAME = os.environ.get('SAUCE_USERNAME')
ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')
sauce = SauceClient(USERNAME, ACCESS_KEY)

browsers = [{
                "platform": "Mac OS X 10.8",
                "browserName": "chrome",
                "version": "31"
            },
            {
                "platform": "Windows 8.1",
                "browserName": "internet explorer",
                "version": "11"
            },
            {
                "platform": "OSX 10.9",
                "browserName": "firefox",
                "version": "beta"
            },
            {
                "platform": "OSX 10.9",
                "browserName": "safari",
                "version": "7"
            },]


@on_platforms(browsers)
class TestPollSauce(unittest.TestCase):
    def setUp(self):
        self.desired_capabilities['name'] = self.id()

        command_executor = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (USERNAME, ACCESS_KEY)
        self.driver = webdriver.Remote(
            desired_capabilities=self.desired_capabilities,
            command_executor=command_executor
        )
        self.driver.implicitly_wait(30)


    def tearDown(self):
        print("Link to your job: https://saucelabs.com/jobs/%s" % self.driver.session_id)
        try:
            if sys.exc_info() == (None, None, None):
                sauce.jobs.update_job(self.driver.session_id, passed=True)
            else:
                sauce.jobs.update_job(self.driver.session_id, passed=False)
        finally:
            self.driver.quit()
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
