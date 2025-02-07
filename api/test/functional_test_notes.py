import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class TestLocalhostNotes(unittest.TestCase):

    def setUp(self):
        """✅ Set up WebDriver, login, and ensure notes table is ready."""
        options = webdriver.ChromeOptions()
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(5)  # Implicit wait of 5s

        # 1. Open Vue.js app
        self.driver.get("http://localhost:5173")

        # 2. Wait for initial page load
        WebDriverWait(self.driver, 10).until(lambda d: d.title != "")
        self.assertIn("CprE Archive", self.driver.title)

        # 3. Click login button (if needed for your auth flow)
        auth_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.nav-card > div.auth-section > button"))
        )
        auth_button.click()

        # 4. Navigate to /notes
        self.driver.get("http://localhost:5173/notes")
        WebDriverWait(self.driver, 10).until(EC.url_contains("/notes"))

        # 5. Wait for the notes table (adjust the selector to match your DOM)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
        )

        # Define test cases
        self.test_cases = [
            {"note": "test_case_001", "pdf": "google-drive.com/note001.pdf", "course": "CS101", "desc": "first test"},
            {"note": "test_case_002", "pdf": "google-drive.com/note002.pdf", "course": "CS101", "desc": "second test"},
            {"note": "test_case_003", "pdf": "google-drive.com/note003.pdf", "course": "CS101", "desc": "third test"},
            {"note": "test_case_004", "pdf": "google-drive.com/note004.pdf", "course": "CS101", "desc": "fourth test"},
            {"note": "test_case_005", "pdf": "google-drive.com/note005.pdf", "course": "CS102", "desc": "fifth test"}
        ]

        # We'll track the "expected" state of the table in self.expected_rows.
        self.expected_rows = []

        # Now add the test notes to ensure they exist for deletion tests:
        self.add_notes()

    def add_notes(self):
        """✅ Adds 5 notes and verifies they appear in row #2 after each add."""
        print("\n[TEST] Adding Notes Before Delete Tests")

        for index, case in enumerate(self.test_cases, start=1):
            # Fill input fields in the "input row" (row 1)
            input_selectors = [
                ("#app > div > div.container > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(1) > input", case["note"]),
                ("#app > div > div.container > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > input", case["pdf"]),
                ("#app > div > div.container > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(3) > input", case["course"]),
                ("#app > div > div.container > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(4) > input", case["desc"])
            ]

            for selector, value in input_selectors:
                input_field = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                input_field.clear()
                input_field.send_keys(value)

            # Click the Add button in the input row (row 1, col 5)
            add_button_selector = (
                "#app > div > div.container > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(5) > button"
            )
            self.driver.find_element(By.CSS_SELECTOR, add_button_selector).click()

            # Short sleep for UI to finish insertion animation
            time.sleep(0.2)

            # ✅ Check that the newly added row (#2) matches our inputs
            check_selectors = [
                (
                    "#app > div > div.container > div > div > div > table > tbody > tr:nth-child(2) > td:nth-child(1) > input",
                    case["note"]
                ),
                (
                    "#app > div > div.container > div > div > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > input",
                    case["pdf"]
                ),
                (
                    "#app > div > div.container > div > div > div > table > tbody > tr:nth-child(2) > td:nth-child(3) > input",
                    case["course"]
                ),
                (
                    "#app > div > div.container > div > div > div > table > tbody > tr:nth-child(2) > td:nth-child(4) > input",
                    case["desc"]
                ),
            ]

            for selector, expected_value in check_selectors:
                input_field = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                actual_value = input_field.get_attribute("value")

                # Now using assertEqual (the correct Python unittest method).
                self.assertEqual(
                    actual_value,
                    expected_value,
                    f"❌ Mismatch after adding note: Expected '{expected_value}', Found '{actual_value}'"
                )

            # Keep track of the row in a "expected_rows" (newest note is top at row #2).
            self.expected_rows.insert(0, case)

    def test_delete_notes(self):
        """✅ Tests deleting the 5 notes and ensuring row shift is correct each time."""
        print("\n[TEST] Running: Delete Notes and Check Shift Up")

        for delete_index in range(5):
            # 1. Click the delete button for the top row (#2 in the table)
            delete_button_selector = (
                "#app > div > div.container > div > div > div > table > tbody > tr:nth-child(2) > td:nth-child(5) > button"
            )
            try:
                delete_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, delete_button_selector))
                )
                delete_button.click()

                # 2. Accept the alert confirmation
                WebDriverWait(self.driver, 5).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                alert.accept()

            except Exception as e:
                print("❌ Could not find delete button at row 2 or confirm box did not appear.")
                raise e

            # 3. Wait for UI to update
            time.sleep(0.2)

            # 4. Update our local expected_rows by removing the topmost row
            if self.expected_rows:
                self.expected_rows.pop(0)
            else:
                # If nothing is expected, stop
                return

            # 5. If rows are still expected, verify the new top row
            if self.expected_rows:
                expected_top = self.expected_rows[0]
                verify_selectors = [
                    (
                        "#app > div > div.container > div > div > div > table > tbody > tr:nth-child(2) > td:nth-child(1) > input",
                        expected_top["note"]
                    ),
                    (
                        "#app > div > div.container > div > div > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > input",
                        expected_top["pdf"]
                    ),
                    (
                        "#app > div > div.container > div > div > div > table > tbody > tr:nth-child(2) > td:nth-child(3) > input",
                        expected_top["course"]
                    ),
                    (
                        "#app > div > div.container > div > div > div > table > tbody > tr:nth-child(2) > td:nth-child(4) > input",
                        expected_top["desc"]
                    ),
                ]

                for selector, expected_value in verify_selectors:
                    input_field = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    actual_value = input_field.get_attribute("value")
                    self.assertEqual(
                        actual_value,
                        expected_value,
                        f"❌ Mismatch after delete: Expected '{expected_value}', Found '{actual_value}'"
                    )

    def tearDown(self):
        """Close the browser after tests."""
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
