import unittest
from selenium import webdriver



class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('/data/work/231/chromedriver')

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Go to the page
        self.browser.get('http://localhost:8000')

        self.assertIn("To-Do", self.browser.title)
        self.fail('Finish the test!')

        # User create item

        # User press enter

        # The page updates. User see results

if __name__ == "__main__":
    unittest.main(warnings="ignore")