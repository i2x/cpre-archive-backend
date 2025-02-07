from django.http import JsonResponse
from django.views import View
from api.models import Course

# 🎯 GET /api/courses/ → Fetch all courses
class CourseListView(View):
    def get(self, request):
        """ Fetch all courses with ID and name """
        courses = Course.objects.all()
        course_data = [{"id": course.id, "name": course.name} for course in courses]
        return JsonResponse({"courses": course_data})
