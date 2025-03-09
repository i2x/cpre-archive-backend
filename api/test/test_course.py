from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CourseTest(StaticLiveServerTestCase):
    def setUp(self):
        # Initialize the Chrome WebDriver.
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_course_crud_flow(self):
        self.driver.get("http://localhost:5173/")

        # ----- Step 1: Login -----
        with self.subTest("Click Get Token Button"):
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#app > div > div.nav-card > div.auth-section > button")
                )
            )
            button.click()

        with self.subTest("Check Username Displayed"):
            username_span = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#app > div > div.nav-card > div.auth-section > span.username")
                )
            )
            self.assertEqual(username_span.text, "sompong")

        # ----- Step 2: Navigate to Course Page -----
        with self.subTest("Click Navigation Link for Course"):
            nav_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#app > div > div.nav-card > div.nav-links > a:nth-child(4)")
                )
            )
            nav_link.click()
        with self.subTest("Check URL changed to /course"):
            WebDriverWait(self.driver, 10).until(
                lambda driver: "/course" in driver.current_url
            )
            self.assertIn("/course", self.driver.current_url)

        # ----- Step 3: Add a New Course (math2 with MA101) -----
        with self.subTest("Add New Course: math2 (MA101)"):
            course_id_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input[placeholder='Enter course ID']")
                )
            )
            course_name_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Enter course name']")
            course_id_input.clear()
            course_id_input.send_keys("MA101")
            course_name_input.clear()
            course_name_input.send_keys("math2")
            add_btn = self.driver.find_element(By.CSS_SELECTOR, "button.btn-success")
            add_btn.click()
            course_id_input.clear()
            course_name_input.clear()

            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element((By.TAG_NAME, "table"), "math2")
            )
            table_text = self.driver.find_element(By.TAG_NAME, "table").text
            self.assertIn("math2", table_text)
            self.assertIn("MA101", table_text)
        
        # ----- Step 4: Edit the Course (change to Linear algebra with LA101) -----
        with self.subTest("Edit Course: change math2 to Linear algebra (LA101)"):
            edit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#app > div > div.container > div > div > div > table > tbody > tr:nth-child(2) > td:nth-child(3) > button.btn.btn-warning.btn-sm")
                )
            )
            edit_btn.click()

            edit_id_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#app > div > div.container > div > div > div > table > tbody > tr:nth-child(2) > td:nth-child(1) > input")
                )
            )
            edit_name_input = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.container > div > div > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > input")
            edit_id_input.clear()
            edit_id_input.send_keys("LA101")
            edit_name_input.clear()
            edit_name_input.send_keys("Linear algebra")

            save_btn = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.container > div > div > div > table > tbody > tr:nth-child(2) > td:nth-child(3) > button.btn.btn-primary.btn-sm")
            save_btn.click()

            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element((By.TAG_NAME, "table"), "Linear algebra")
            )
            table_text = self.driver.find_element(By.TAG_NAME, "table").text
            self.assertIn("Linear algebra", table_text)
            self.assertIn("LA101", table_text)

        # ----- Step 5: Delete the Course -----
        with self.subTest("Delete Course: Linear algebra (LA101)"):
            delete_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#app > div > div.container > div > div > div > table > tbody > tr:nth-child(2) > td:nth-child(3) > button.btn.btn-danger.btn-sm.ms-1")
                )
            )
            delete_btn.click()

            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()

            WebDriverWait(self.driver, 10).until_not(
                EC.text_to_be_present_in_element((By.TAG_NAME, "table"), "Linear algebra")
            )
            table_text = self.driver.find_element(By.TAG_NAME, "table").text
            self.assertNotIn("Linear algebra", table_text)
