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
            print("✅ Clicked Get Token Button")

        # Step 2: ตรวจสอบว่า Username 'tester' ปรากฏ
        with self.subTest("Check Username Displayed"):
            username_span = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div > div.nav-card > div.auth-section > span.username"))
            )
            self.assertEqual(username_span.text, "tester")
            print("✅ Username 'tester' is displayed")

        # Step 3: กด Navigation ไปที่ /notes
        with self.subTest("Click Navigation Link"):
            nav_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.nav-card > div.nav-links > a:nth-child(3)"))
            )
            nav_link.click()
            print("✅ Clicked Navigation Link")

        # Step 4: ตรวจสอบว่า URL เปลี่ยนเป็น /notes
        with self.subTest("Check URL changed to /notes"):
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.current_url == "http://localhost:5173/notes"
            )
            self.assertEqual(self.driver.current_url, "http://localhost:5173/notes")
            print("✅ URL changed to /notes")

        # Step 5: ใส่ข้อมูลลงในแถวแรก
        note_data = {
            "note": "test_case_001",
            "pdf": "google-drive.com/note001.pdf",
            "course": "CS101",
            "desc": "first test"
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

            print("✅ Filled in note details")

        # Step 6: กดปุ่มบันทึก
        with self.subTest("Click Save Button"):
            save_button = self.driver.find_element(By.CSS_SELECTOR, "table > tbody > tr:nth-child(1) > td:nth-child(5) > button")
            save_button.click()
            print("✅ Clicked Save Button")

        # Step 7: ตรวจสอบว่าข้อมูลปรากฏในบรรทัดที่ 2
        with self.subTest("Verify second row data matches input"):
            note_cell = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table > tbody > tr:nth-child(2) > td:nth-child(1)"))
            )
            self.assertEqual(note_cell.text, note_data["note"])
            print("✅ Verified initial note data in Row 2")

        # Step 8: กดปุ่มแก้ไข (Edit) บรรทัดที่ 2
        with self.subTest("Click Edit Button on Row 2"):
            edit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "table > tbody > tr:nth-child(2) > td:nth-child(5) > button.btn.btn-warning.btn-sm"))
            )
            edit_button.click()
            print("✅ Clicked Edit Button on Row 2")

        # Step 9: แก้ไขค่าในช่อง Note (เปลี่ยนเป็น 'test_case_001_edit_here')
        with self.subTest("Edit Note Input in Row 2"):
            edit_note_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table > tbody > tr:nth-child(2) > td:nth-child(1) > input"))
            )
            edit_note_input.clear()
            edit_note_input.send_keys("test_case_001_edit_here")
            print("✅ Updated Note Input to 'test_case_001_edit_here'")

        # Step 10: กดปุ่มบันทึก (Save)
        with self.subTest("Click Save Button on Row 2"):
            save_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "table > tbody > tr:nth-child(2) > td:nth-child(5) > button.btn.btn-primary.btn-sm"))
            )
            save_button.click()
            print("✅ Clicked Save Button on Row 2")

        # Step 11: ตรวจสอบว่าข้อมูลในบรรทัดที่ 2 อัปเดตถูกต้อง
        with self.subTest("Verify Updated Note in Row 2"):
            updated_note = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table > tbody > tr:nth-child(2) > td:nth-child(1)"))
            )
            self.assertEqual(updated_note.text, "test_case_001_edit_here")
            print("✅ Verified Note is updated to 'test_case_001_edit_here'")

       # Step 12: Click Navigation to search page
        with self.subTest("Click Navigation to Search Page"):
            search_nav_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.nav-card > div.nav-links > a:nth-child(1)"))
            )
            search_nav_link.click()
            print("✅ Clicked Navigation to Search Page")

        # Step 13: Fill input field with '001_edit_here'
        with self.subTest("Fill Search Input"):
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div > div.container > div > div.input-group.w-50.mx-auto > input"))
            )
            search_input.clear()
            search_input.send_keys("001_edit_here")
            print("✅ Filled Search Input with '001_edit_here'")

        # Step 14: Click Search Button
        with self.subTest("Click Search Button"):
            search_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.container > div > div.input-group.w-50.mx-auto > button"))
            )
            search_button.click()
            print("✅ Clicked Search Button")

        # Step 15: Verify search result contains expected note
        with self.subTest("Verify Search Result"):
            result_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div > div.container > div > div:nth-child(3) > ul > li:nth-child(1) > div > div.me-3 > strong"))
            )
            self.assertEqual(result_text.text, "test_case_001_edit_here")
            print("✅ Verified Search Result contains 'test_case_001_edit_here'")


       # Step 16: Click Navigation to search page
        with self.subTest("Click Navigation to Search Page"):
            search_nav_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.nav-card > div.nav-links > a:nth-child(3)"))
            )
            search_nav_link.click()
            print("✅ Clicked Navigation to Search Page")
        
                # Step 17: Click Delete Button for the second row note
        with self.subTest("Click Delete Button on Row 2 and Accept Alert"):
            delete_button = WebDriverWait(self.driver, 10).until(
               EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.container > div > div > div > table > tbody > tr:nth-child(2) > td:nth-child(5) > button.btn.btn-danger.btn-sm.ms-1"))
               )
            delete_button.click()
            print("✅ Clicked Delete Button on Row 2")

                # Handle alert popup
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            print("✅ Accepted Alert")
        # Step 18: Navigate back to the Search Page
        with self.subTest("Navigate Back to Search Page"):
            search_nav_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.nav-card > div.nav-links > a:nth-child(1)"))
        )
        search_nav_link.click()
        print("✅ Navigated Back to Search Page")

        # Step 19: Fill Search Input Again with the Same Query
        with self.subTest("Fill Search Input After Deletion"):
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div > div.container > div > div.input-group.w-50.mx-auto > input"))
            )
            search_input.clear()
            search_input.send_keys("001_edit_here")
            print("✅ Re-entered Search Query '001_edit_here'")

        # Step 20: Click Search Button
        with self.subTest("Click Search Button Again"):
            search_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.container > div > div.input-group.w-50.mx-auto > button"))
            )
            search_button.click()
            print("✅ Clicked Search Button Again")

        # Step 21: Verify No Search Results After Deletion
        with self.subTest("Verify No Search Results After Deletion"):

            no_files_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'No files found.')]"))
            )
            self.assertIsNotNone(no_files_element, "❌ 'No files found.' message not found!")
            print("✅ Verified 'No files found.' message appears after deletion")