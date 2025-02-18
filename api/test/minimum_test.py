from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class SearchTest(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_search_functionality(self):
        self.driver.get("http://localhost:5173/")

        # Search by Name (Software)
        search_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div > div.container > div > div.input-group.w-50.mx-auto > input"))
        )
        search_input.clear()
        search_input.send_keys("Software")

        search_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.container > div > div.input-group.w-50.mx-auto > button"))
        )
        search_button.click()
        time.sleep(0.1)

        #Verify search result contains expected note details
        with self.subTest("Verify Search Result Details"):
            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#app > div > div.container > div > div:nth-child(3) > ul > li:nth-child(1) > div > div.me-3"))
            )   
        elements_text = elements[0].text.split("\n")
        
        note_title = elements_text[0]
        owner_text = elements_text[1]
        course_text = elements_text[2]

        self.assertEqual(note_title, "Software Engineering Notes", f"Expected 'Software Engineering Notes' but got '{note_title}'")
        self.assertEqual(owner_text, "Owned by: sompong", f"Expected 'Owned by: sompong' but got '{owner_text}'")
        self.assertEqual(course_text, "Software Engineering Principles", f"Expected 'Software Engineering Principles' but got '{course_text}'")


        # Search by Tag (Data Structures)
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.container > div > div.input-group.w-50.mx-auto > select"))
        )
        dropdown.click()

        tag_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//option[@value='tags']"))
        )
        tag_option.click()

        search_input.clear()
        search_input.send_keys("data structures")
        search_button.click()

        result_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div > div.container > div > div:nth-child(3) > ul > li:nth-child(1) > div > div.me-3 > strong"))
        )
        self.assertEqual(result_text.text, "Data Structures Guide")
        # search not found
        search_input.clear()
        search_input.send_keys("math")
        search_button.click()

        no_files_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'No files found.')]"))
        )
        self.assertIsNotNone(no_files_element)

class NoteTest(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_note_editing_and_deletion(self):
        self.driver.get("http://localhost:5173/")
       # กดปุ่ม Get Token
        with self.subTest("Click Get Token Button"):
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.nav-card > div.auth-section > button"))
            )
            button.click()

        # ตรวจสอบว่า Username 'sompong' ปรากฏ
        with self.subTest("Check Username Displayed"):
            username_span = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div > div.nav-card > div.auth-section > span.username"))
            )
            self.assertEqual(username_span.text, "sompong")

        # Navigate to Notes Page
        with self.subTest("Click Navigation Link"):
            nav_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.nav-card > div.nav-links > a:nth-child(3)"))
            )
            nav_link.click()

        # ตรวจสอบว่า URL เปลี่ยนเป็น /notes
        with self.subTest("Check URL changed to /notes"):
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.current_url == "http://localhost:5173/notes"
            )
            self.assertEqual(self.driver.current_url, "http://localhost:5173/notes")

        # Add new note
        note_data = {
            "note": "math",
            "pdf": "google-drive.com/note001.pdf",
            "course": "CS101",
            "desc": "calculus"
        }

        note_input = self.driver.find_element(By.CSS_SELECTOR, "table > tbody > tr:nth-child(1) > td:nth-child(1) > input")
        pdf_input = self.driver.find_element(By.CSS_SELECTOR, "table > tbody > tr:nth-child(1) > td:nth-child(2) > input")
        course_input = self.driver.find_element(By.CSS_SELECTOR, "table > tbody > tr:nth-child(1) > td:nth-child(3) > input")
        desc_input = self.driver.find_element(By.CSS_SELECTOR, "table > tbody > tr:nth-child(1) > td:nth-child(4) > input")

        note_input.clear()
        note_input.send_keys(note_data["note"])
        pdf_input.clear()
        pdf_input.send_keys(note_data["pdf"])
        course_input.clear()
        course_input.send_keys(note_data["course"])
        desc_input.clear()
        desc_input.send_keys(note_data["desc"])

        save_button = self.driver.find_element(By.CSS_SELECTOR, "table > tbody > tr:nth-child(1) > td:nth-child(5) > button")
        save_button.click()
        time.sleep(0.1)
        
        # ตรวจสอบว่าข้อมูลปรากฏในบรรทัดที่ 2
        with self.subTest("Verify second row data matches input"):
            note_cell = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table > tbody > tr:nth-child(2) > td:nth-child(1)"))
            )
            self.assertEqual(note_cell.text, note_data["note"])

        # Edit note
        edit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "table > tbody > tr:nth-child(2) > td:nth-child(5) > button:nth-child(1)"))
        )
        edit_button.click()

        edit_note_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table > tbody > tr:nth-child(2) > td:nth-child(1) > input"))
        )
        edit_note_input.clear()
        edit_note_input.send_keys("math2")

        save_button = self.driver.find_element(By.CSS_SELECTOR, "table > tbody > tr:nth-child(2) > td:nth-child(5) > button:nth-child(1)")
        save_button.click()
        time.sleep(0.1)
        #verify update note
        updated_note = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table > tbody > tr:nth-child(2) > td:nth-child(1)"))
        )
        self.assertEqual(updated_note.text, "math2")

        # Delete note
        delete_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "table > tbody > tr:nth-child(2) > td:nth-child(5) > button.btn.btn-sm.ms-1"))
        )
        delete_button.click()

        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.accept()
        time.sleep(0.1)

        # Verify note is deleted (should not find "math2" in the table anymore)
        with self.subTest("Verify note 'math2' is deleted"):
            table_text = self.driver.find_element(By.CSS_SELECTOR, "table > tbody").text
            self.assertNotIn("math2", table_text)
