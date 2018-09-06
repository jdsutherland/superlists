from selenium import webdriver
from .base import FunctionalTest, CHROME_OPTIONS
from .list_page import ListPage


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):
    def test_can_share_a_list_with_another_user(self):
        # Alice is a logged-in user
        self.create_pre_authenticated_session('alice@example.com')
        alice_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(alice_browser))

        # Her friend Oniciferous is also hanging out on the lists site
        oni_browser = webdriver.Chrome(chrome_options=CHROME_OPTIONS)
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.browser = oni_browser
        self.create_pre_authenticated_session('oniciferous@example.com')

        # Alice goes to the home page and starts a list
        self.browser = alice_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item('Get help')

        # She notices a "Share this list" option
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'), 'your-friend@example.com')

        # She shares her list.
        # The page updates to say that it's shared with Oniciferous:
        list_page.share_list_with('oniciferous@example.com')

        # Oniciferous now goes to the lists page with his browser
        self.browser = oni_browser
        MyListsPage(self).go_to_my_lists_page()

        # He sees Alice's list in there!
        self.browser.find_element_by_link_text('Get help').click()

        # On the list page, Oniciferous can see says that it's Alice's list
        self.wait_for(
            lambda: self.assertEqual(list_page.get_list_owner(), 'alice@example.com')
        )

        # He adds an item to the list
        list_page.add_list_item('Hi Alice!')

        # When Alice refreshes the page, she sees Oniciferous's addition
        self.browser = alice_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('Hi Alice!', 2)
