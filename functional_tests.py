import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(chrome_options=chrome_options)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retreive_it_later(self):
        # visit homepage
        self.browser.get('http://localhost:8000')

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
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows))

        # There is still a textbox inviting her to add another item.
        #   She enters 'Use peacock feathers to make fly'
        self.assertFail('Finish the test!')


if __name__ == "__main__":
    unittest.main(warnings='ignore')
