import time
import unittest

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(chrome_options=chrome_options)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_list_in_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retreive_it_later(self):
        # visit homepage
        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)
        self.assertIn('To-Do',
                      self.browser.find_element_by_tag_name('h1').text)

        # she's invited to enter a to-do item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # She types 'Buy peacock feathers' into a textbox
        inputbox.send_keys('Buy peacock feathers')
        # when she hits ENTER, the page updates & the page lists the to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_list_in_table('1: Buy peacock feathers')
        self.check_for_row_list_in_table(
            '2: Use peacock feathers to make a fly')

        # There is still a textbox inviting her to add another item.
        #   She enters 'Use peacock feathers to make fly'
        self.fail('Finish the test!')
