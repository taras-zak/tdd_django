import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('/data/work/231/chromedriver')

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn( row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Go to the page
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)

        # The page updates. User see results
        self.check_for_row_in_list_table('1: Build home')

        # User try add another item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Plant tree')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Page updates  again, and shows two items
        self.check_for_row_in_list_table('1: Build home')
        self.check_for_row_in_list_table('2: Plant tree')


        self.fail('Finish the test!')



if __name__ == "__main__":
    unittest.main(warnings="ignore")