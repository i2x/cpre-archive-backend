from django.http import JsonResponse
from django.views import View
from api.models import Course
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
import json

# 🎯 GET /api/courses/ → Fetch all courses
class CourseListView(View):
    def get(self, request):
        """ Fetch all courses with ID and name """
        courses = Course.objects.all()
        course_data = [{"id": course.id, "name": course.name} for course in courses]
        return JsonResponse({"courses": course_data})

class CourseDetailView(View):
    def get(self, request, course_id):
        """Fetch 1 course with string ID"""
        course = get_object_or_404(Course, id=course_id)
        course_data = {
            "id": course.id,
            "name": course.name,
        }
        return JsonResponse({
            "message": "Course retrieved successfully",
            "course": course_data
        })

    def delete(self, request, course_id):
        """Delete a course by string ID"""
        course = get_object_or_404(Course, id=course_id)
        course.delete()
        return JsonResponse({
            "message": "Course deleted successfully"
        }, status=204)

    def put(self, request, course_id):
        """Update course details, allowing ID change but ensuring uniqueness"""
        course = get_object_or_404(Course, id=course_id)

        try:
            data = json.loads(request.body)  # Parse JSON request body
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON format"}, status=400)

        # เช็คว่ามีการอัปเดต ID หรือไม่
        new_id = data.get("id", course_id)
        if new_id != course_id:
            if Course.objects.filter(id=new_id).exists():
                return JsonResponse({"message": "Course ID already exists"}, status=400)
            course.id = new_id  # เปลี่ยน ID ได้ถ้าไม่ซ้ำ

        # อัปเดตชื่อหลักสูตรหากมีการส่งมา
        if "name" in data:
            course.name = data["name"]

        course.save()  # บันทึกการเปลี่ยนแปลง

        updated_data = {
            "id": course.id,
            "name": course.name,
        }
        return JsonResponse({
            "message": "Course updated successfully",
            "course": updated_data
        })

class CourseCreateView(View):
    def post(self, request):
        """Create a new course"""
        try:
            data = json.loads(request.body)  # Load JSON data
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON format"}, status=400)

        # Validate required fields
        if "id" not in data or "name" not in data:
            return JsonResponse({"message": "Missing required fields: 'id' and 'name'"}, status=400)

        # Check if the course ID already exists
        if Course.objects.filter(id=data["id"]).exists():
            return JsonResponse({"message": "Course ID already exists"}, status=400)

        # Create new course
        course = Course.objects.create(
            id=data["id"],
            name=data["name"]
        )

        # Return success response
        return JsonResponse({
            "message": "Course created successfully",
            "course": {
                "id": course.id,
                "name": course.name
            }
        }, status=201)

