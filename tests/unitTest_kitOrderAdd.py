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

        link = 'https://automatedtestlink.com'

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
        time.sleep(2)

        # Access the study details page for the test study
        driver.get("http://127.0.0.1:8000/KITS/study/4/study_detail/")
        time.sleep(2)
        driver.get("http://127.0.0.1:8000/KITS/study/4/kit_ordering_add/")
        elem = driver.find_element_by_id("id_type")
        elem.click()
        elem = driver.find_element_by_xpath("/html/body/div/form/p[1]/select/option[1]")
        elem.click()
        elem = driver.find_element_by_id("id_link")
        elem.send_keys(link)
        time.sleep(1)
        elem.send_keys(Keys.RETURN)
        time.sleep(2)

        # assert "Add Kit Ordering"
        try:
            # attempt to find the 'Add Kit Ordering' header - if found, kit order info successfully added
            elem = driver.find_element_by_xpath("//*[@id='kit_order_info']")

            assert True

        except NoSuchElementException:
            self.fail("Add Kit Order Info failed - Study may not exist or kit ordering info may not have been added")
            assert False

        time.sleep(3)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
