from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class MinimumTest(StaticLiveServerTestCase):
    def setUp(self):
        """Setup Selenium WebDriver"""
        self.driver = webdriver.Chrome()  # ใช้ ChromeDriver
        self.driver.implicitly_wait(10)  # รอ 10 วินาทีถ้า Element ยังไม่มา

    def tearDown(self):
        """Close browser after test"""
        self.driver.quit()

    def test_authentication_and_note_editing(self):
        """ทดสอบ Login, Navigation, การเพิ่ม Note และการแก้ไข Note"""
        self.driver.get("http://localhost:5173/")  # เปิดเว็บ Vue.js

        # Step 1: กดปุ่ม Get Token
        with self.subTest("Click Get Token Button"):
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.nav-card > div.auth-section > button"))
            )
            button.click()


        # Step 2: ตรวจสอบว่า Username 'sompong' ปรากฏ
        with self.subTest("Check Username Displayed"):
            username_span = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div > div.nav-card > div.auth-section > span.username"))
            )
            self.assertEqual(username_span.text, "sompong")


        # Step 3: กด Navigation ไปที่ /notes
        with self.subTest("Click Navigation Link"):
            nav_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.nav-card > div.nav-links > a:nth-child(3)"))
            )
            nav_link.click()

        # Step 4: ตรวจสอบว่า URL เปลี่ยนเป็น /notes
        with self.subTest("Check URL changed to /notes"):
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.current_url == "http://localhost:5173/notes"
            )
            self.assertEqual(self.driver.current_url, "http://localhost:5173/notes")

        # Step 5: ใส่ข้อมูลลงในแถวแรก
        note_data = {
            "note": "math",
            "pdf": "google-drive.com/note001.pdf",
            "course": "CS101",
            "desc": "calculus"
        }

        with self.subTest("Fill in note details"):
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


        # Step 6: กดปุ่มบันทึก
        with self.subTest("Click Save Button"):
            save_button = self.driver.find_element(By.CSS_SELECTOR, "table > tbody > tr:nth-child(1) > td:nth-child(5) > button")
            save_button.click()
            time.sleep(0.1)

        # Step 7: ตรวจสอบว่าข้อมูลปรากฏในบรรทัดที่ 2
        with self.subTest("Verify second row data matches input"):
            note_cell = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table > tbody > tr:nth-child(2) > td:nth-child(1)"))
            )
            self.assertEqual(note_cell.text, note_data["note"])

        # Step 8: กดปุ่มแก้ไข (Edit) บรรทัดที่ 2
        with self.subTest("Click Edit Button on Row 2"):
            edit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.container > div > div > div > table > tbody > tr:nth-child(2) > td:nth-child(5) > button:nth-child(1)"))
            )
            edit_button.click()

        # Step 9: แก้ไขค่าในช่อง Note (เปลี่ยนเป็น 'math2')
        with self.subTest("Edit Note Input in Row 2"):
            edit_note_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table > tbody > tr:nth-child(2) > td:nth-child(1) > input"))
            )
            edit_note_input.clear()
            edit_note_input.send_keys("math2")

        # Step 10: กดปุ่มบันทึก (Save)
        with self.subTest("Click Save Button on Row 2"):
            save_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.container > div > div > div > table > tbody > tr:nth-child(2) > td:nth-child(5) > button:nth-child(1)"))
            )
            save_button.click()
            time.sleep(0.1)
        # Step 11: ตรวจสอบว่าข้อมูลในบรรทัดที่ 2 อัปเดตถูกต้อง
        with self.subTest("Verify Updated Note in Row 2"):
            updated_note = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table > tbody > tr:nth-child(2) > td:nth-child(1)"))
            )
            
            self.assertEqual(updated_note.text, "math2")

       # Step 12: Click Navigation to search page
        with self.subTest("Click Navigation to Search Page"):
            search_nav_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.nav-card > div.nav-links > a:nth-child(1)"))
            )
            search_nav_link.click()

        # Step 13: Fill input field with 'math'
        with self.subTest("Fill Search Input"):
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div > div.container > div > div.input-group.w-50.mx-auto > input"))
            )
            search_input.clear()
            search_input.send_keys("math")

        # Step 14: Click Search Button
        with self.subTest("Click Search Button"):
            search_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.container > div > div.input-group.w-50.mx-auto > button"))
            )
            search_button.click()

        # Step 15: Verify search result contains expected note details
        with self.subTest("Verify Search Result Details"):
            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#app > div > div.container > div > div:nth-child(3) > ul > li:nth-child(1) > div > div.me-3"))
            )   
        elements_text = elements[0].text.split("\n")
        
        note_title = elements_text[0]
        owner_text = elements_text[1]
        course_text = elements_text[2]

        self.assertEqual(note_title, "math2", f"Expected 'math2' but got '{note_title}'")
        self.assertEqual(owner_text, "Owned by: sompong", f"Expected 'Owned by: sompong' but got '{owner_text}'")
        self.assertEqual(course_text, "Introduction to Computer Science", f"Expected 'Introduction to Computer Science' but got '{course_text}'")


        # Step 16: Click on dropdown to select 'Tags'
        with self.subTest("Click on search dropdown"):
            dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.container > div > div.input-group.w-50.mx-auto > select"))
            )
            dropdown.click()

        # Step 17: Select 'Tags' from dropdown
        with self.subTest("Select 'Tags' option from dropdown"):
            tag_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//option[@value='tags']"))
             )
            tag_option.click()
            time.sleep(1)

        # Step 18: Enter search query 'data structures'
        with self.subTest("Enter search query 'data structures'"):
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div > div.container > div > div.input-group.w-50.mx-auto > input"))
            )
            search_input.clear()
            search_input.send_keys("guide")
            time.sleep(1)

        # Step 19: Click Search Button_
        with self.subTest("Click Search Button"):
            search_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.container > div > div.input-group.w-50.mx-auto > button"))
            )
            search_button.click()
            time.sleep(1)

        # Step 20: Verify search result contains 'Data Structures Guide'
        with self.subTest("Verify search result contains 'Data Structures Guide'"):
            result_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div > div.container > div > div:nth-child(3) > ul > li:nth-child(1) > div > div.me-3 > strong"))
            )
            self.assertEqual(result_text.text, "Data Structures Guide")
       # Step 21: Click Navigation to note page
        with self.subTest("Click Navigation to Note Page"):
            search_nav_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.nav-card > div.nav-links > a:nth-child(3)"))
            )
            search_nav_link.click()
        
        # Step 22: Click Delete Button for the second row note
        with self.subTest("Click Delete Button on Row 2 and Accept Alert"):
            delete_button = WebDriverWait(self.driver, 10).until(
               EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.container > div > div > div > table > tbody > tr:nth-child(2) > td:nth-child(5) > button.btn.btn-sm.ms-1"))
               )
            delete_button.click()

        # Handle alert popup
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
        # Step 23: Navigate back to the Search Page
        with self.subTest("Navigate Back to Search Page"):
            search_nav_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.nav-card > div.nav-links > a:nth-child(1)"))
        )
        search_nav_link.click()

        # Step 24: Fill Search Input Again with the Same Query
        with self.subTest("Fill Search Input After Deletion"):
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div > div.container > div > div.input-group.w-50.mx-auto > input"))
            )
            search_input.clear()
            search_input.send_keys("math")
        # Step 25: Click Search Button
        with self.subTest("Click Search Button Again"):
            search_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.container > div > div.input-group.w-50.mx-auto > button"))
            )
            search_button.click()


        # Step 26: Verify No Search Results After Deletion
        with self.subTest("Verify No Search Results After Deletion"):

            no_files_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'No files found.')]"))
            )
            self.assertIsNotNone(no_files_element, "❌ 'No files found.' message not found!")
