from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from api.models import Course

class CourseListView(APIView):
    def get(self, request):
        """Fetch all courses with ID and name"""
        courses = Course.objects.all()
        course_data = [{"id": course.id, "name": course.name} for course in courses]
        return Response({"courses": course_data}, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new course"""
        data = request.data  # DRF handles JSON parsing

        if "id" not in data or "name" not in data:
            return Response({"message": "Missing required fields: 'id' and 'name'"}, status=status.HTTP_400_BAD_REQUEST)

        if Course.objects.filter(id=data["id"]).exists():
            return Response({"message": "Course ID already exists"}, status=status.HTTP_400_BAD_REQUEST)

        course = Course.objects.create(id=data["id"], name=data["name"])
        return Response({
            "message": "Course created successfully",
            "course": {"id": course.id, "name": course.name}
        }, status=status.HTTP_201_CREATED)
    
class CourseDetailView(APIView):
    def get(self, request, course_id):
        """Fetch 1 course with string ID"""
        course = get_object_or_404(Course, id=course_id)
        course_data = {"id": course.id, "name": course.name}
        return Response({
            "message": "Course retrieved successfully",
            "course": course_data
        }, status=status.HTTP_200_OK)

    def delete(self, request, course_id):
        """Delete a course by string ID"""
        course = get_object_or_404(Course, id=course_id)
        course.delete()
        return Response({"message": "Course deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, course_id):
        """Update course details, allowing ID change but ensuring uniqueness"""
        course = get_object_or_404(Course, id=course_id)
        data = request.data  # DRF automatically parses JSON

        new_id = data.get("id", course_id)
        if new_id != course_id and Course.objects.filter(id=new_id).exists():
            return Response({"message": "Course ID already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        if new_id != course_id:
            course.id = new_id  # Update ID if unique
        
        if "name" in data:
            course.name = data["name"]
        
        course.save()
        
        return Response({
            "message": "Course updated successfully",
            "course": {"id": course.id, "name": course.name}
        }, status=status.HTTP_200_OK)


