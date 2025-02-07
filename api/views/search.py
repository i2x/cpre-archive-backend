from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from api.models import Note

class SearchNotesView(View):
    def get(self, request):
        query = request.GET.get("q", "").strip()
        field = request.GET.get("field", "name")  # ใช้ "name" เป็นค่าเริ่มต้น
        if not query:
            return JsonResponse({"error": "Missing query parameter 'q'"}, status=400)

        # ✅ อนุญาตให้ค้นหาเฉพาะฟิลด์ที่กำหนดใน whitelist เพื่อป้องกัน SQL Injection
        allowed_fields = ["name", "tags", "user__username", "course__name"]
        if field not in allowed_fields:
            return JsonResponse({"error": f"Invalid search field '{field}'"}, status=400)

        # ✅ ค้นหาตามฟิลด์ที่ผู้ใช้กำหนด
        filter_kwargs = {f"{field}__icontains": query}
        notes = Note.objects.filter(**filter_kwargs)

        notes_data = [
            {
                "id": note.id,
                "name": note.name,
                "file_url": note.file_url,
                "thumbnail_url": note.thumbnail_url,
                "tags": note.tags,
                "user": note.user.username,
                "course": note.course.name,
                "created_at": note.created_at,
                "updated_at": note.updated_at
            }
            for note in notes
        ]

        return JsonResponse({"results": notes_data})
