from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Max
from api.models import Curriculum, CurriculumMapping
from django.views import View


class CurriculumCoursesView(View):
    def get(self, request, curriculum_id=None):
        # ถ้าไม่มี curriculum_id ให้ใช้หลักสูตรล่าสุด
        if curriculum_id is None:
            curriculum = Curriculum.objects.order_by('-year', '-id').first()
            if not curriculum:
                return JsonResponse({"error": "No curriculum found"}, status=404)
        else:
            curriculum = get_object_or_404(Curriculum, pk=curriculum_id)

        mappings = CurriculumMapping.objects.filter(curriculum=curriculum).select_related("course")

        courses = [
            {
                "id": mapping.course.id,
                "name": mapping.course.name,
                "year": mapping.year,
                "term": mapping.term
            }
            for mapping in mappings
        ]

        return JsonResponse({"curriculum": curriculum.name, "courses": courses})