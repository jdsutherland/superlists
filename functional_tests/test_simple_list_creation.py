from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_for_one_user(self):
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
        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Alice is very
        # methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table(
            '2: Use peacock feathers to make a fly')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Alice start a new todo list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # She notices that her list has a unique URL
        alice_list_url = self.browser.current_url
        self.assertRegex(alice_list_url, '/lists/.+')

        # Now a new user, Bob, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Alice's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Bob visits the home page.  There is no sign of Alice's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Bob starts a new list by entering a new item. He
        # is less interesting than Alice...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Bob gets his own unique URL
        bob_list_url = self.browser.current_url
        self.assertRegex(bob_list_url, '/lists/.+')
        self.assertNotEqual(bob_list_url, alice_list_url)

        # Again, there is no trace of Alice's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep
