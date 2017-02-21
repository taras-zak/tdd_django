import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('/data/work/231/chromedriver')

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        #Go to the page
        self.browser.get(self.live_server_url)

        # Check page title
        self.assertIn("To-Do", self.browser.title)

        # Check header
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # User find inputbox
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEquals(
            inputbox.get_attribute('placeholder'),
            'Enter to-do item'
        )

        # User create item
        inputbox.send_keys('Build home')

        # User press enter
        inputbox.send_keys(Keys.ENTER)

        # The page updates. User see results
        self.wait_for_row_in_list_table('1: Build home')

        # User try add another item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Plant tree')
        inputbox.send_keys(Keys.ENTER)

        # Page updates  again, and shows two items
        self.wait_for_row_in_list_table('1: Build home')
        self.wait_for_row_in_list_table('2: Plant tree')

        # end


    def test_multiple_users_can_start_lists_at_different_urls(self):

        # First user create todo list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy ticket')
        inputbox.send_keys(Keys.ENTER)

        # Page updates  again, and shows two items
        self.wait_for_row_in_list_table('1: Buy ticket')

        first_user_list_url = self.browser.current_url
        self.assertRegex(first_user_list_url, '/lists/.+')

        # New user want to create list

        # First user gone
        self.browser.quit()
        self.browser = webdriver.Chrome('/data/work/231/chromedriver')

        # Second user come
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("Buy honey", page_text)
        self.assertNotIn("make a trip", page_text)

        # He create new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy honey')

        # Check his own url
        second_user_url = self.browser.current_url
        self.assertRegex(second_user_url, '/lists/.+')
        self.assertNotEqual(second_user_url, first_user_list_url)

        self.assertNotIn("Buy ticket", page_text)
        self.assertIn("Buy honey", page_text)

        # Second user go away




