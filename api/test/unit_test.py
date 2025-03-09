import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models.course import Course
from api.models.curriculum import Curriculum, CurriculumMapping
from api.models.note import Note
from api.models.user import CustomUser


class APITest(APITestCase):
    def setUp(self):
        # สร้างผู้ใช้งานทดสอบ
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass"
        )
        # Authenticate user สำหรับการทดสอบ API
        self.client.force_authenticate(user=self.user)

        # สร้าง Course ทดสอบ
        self.course = Course.objects.create(
            id="CSE101",
            name="Introduction to Computer Science"
        )

        # สร้าง Curriculum และ Mapping
        self.curriculum = Curriculum.objects.create(
            id="CURR2025",
            name="Curriculum 2025",
            year=2025
        )
        self.curriculum_mapping = CurriculumMapping.objects.create(
            curriculum=self.curriculum,
            course=self.course,
            year=2025,
            term=1
        )

        # สร้าง Note ทดสอบ
        self.note = Note.objects.create(
            name="Test Note",
            file_url="http://example.com/note.pdf",
            user=self.user,
            course=self.course,
            tags="test,note"
        )

    # ทดสอบ Get Token by Email endpoint
    def test_get_token_by_email(self):
        url = reverse('get-token')
        data = {"email": self.user.email}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)

    # 🎯 Course API Tests

    def test_create_course(self):
        url = reverse('course-list')
        data = {"id": "MATH101", "name": "Calculus I"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Course.objects.filter(id="MATH101").exists())

    def test_get_course_detail(self):
        url = reverse('course-detail', kwargs={"course_id": self.course.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ใช้ response.json() แทน response.data
        data = response.json()
        # หาก response ถูกห่ออยู่ภายใน key "course" ให้ดึงข้อมูลออกมา
        course_data = data.get("course", data)
        self.assertEqual(course_data.get("name"), self.course.name)

    def test_update_course_detail(self):
        url = reverse('course-detail', kwargs={"course_id": self.course.id})
        data = {"name": "Intro to CS Updated"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.name, "Intro to CS Updated")

    def test_delete_course_detail(self):
        url = reverse('course-detail', kwargs={"course_id": self.course.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(pk=self.course.id)

    # 🎯 Curriculum API Test
    def test_get_curriculum_courses(self):
        url = reverse('curriculum-latest')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ใช้ response.json() เพื่อดึงข้อมูล JSON ออกมา
        data = response.json()
        self.assertGreaterEqual(len(data), 1)

    # 🎯 Note API Tests
    def test_list_create_note(self):
        url = reverse('note-list-create')
        # ทดสอบเรียกดู list
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ทดสอบสร้าง Note ใหม่ โดยใช้ key "course_id" แทน "course"
        data = {
            "name": "New Note",
            "file_url": "http://example.com/new_note.pdf",
            "course_id": self.course.id,
            "tags": "new,note"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Note.objects.filter(name="New Note").exists())

    def test_note_detail_view(self):
        url = reverse('note-detail', kwargs={"pk": self.note.pk})
        # ดึงข้อมูล Note
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), self.note.name)
        # ทดสอบอัปเดต Note
        update_data = {"name": "Updated Note"}
        response = self.client.put(url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertEqual(self.note.name, "Updated Note")
        # ทดสอบลบ Note
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(pk=self.note.pk)




