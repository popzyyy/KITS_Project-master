import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class ll_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_ll(self):
        user = "instructor"
        pwd = "Mavericks"

        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/KITS")
        time.sleep(2)
        driver.get("http://127.0.0.1:8000/accounts/login")
        elem = driver.find_element_by_id("id_username")
        elem.send_keys(user)
        elem = driver.find_element_by_id("id_password")
        elem.send_keys(pwd)
        time.sleep(2)
        elem.send_keys(Keys.RETURN)
        time.sleep(2)
        driver.get("http://127.0.0.1:8000/KITS/study_list/")

        # assert "Study List"
        try:
            # attempt to find the 'Study List' header - if found, study list page is displayed
            elem = driver.find_element_by_xpath("//*[@id='study_list']")

            assert True

        except NoSuchElementException:
            self.fail("Study List not found - May be on the wrong page.")
            assert False

        time.sleep(3)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
