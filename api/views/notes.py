from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from api.models import Note, Course
from rest_framework import status


class NoteListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """ Fetch only the notes of the logged-in user """
        notes = Note.objects.filter(user=request.user).order_by("-created_at")
        notes_data = [
            {
                "id": note.id,
                "name": note.name,
                "file_url": note.file_url,
                "course_id": note.course.id,
                "course_name": note.course.name,
                "user": note.user.username,
                "tags": note.tags,
                "created_at": note.created_at,
                "updated_at": note.updated_at,
            }
            for note in notes
        ]
        return Response({"notes": notes_data})

    def post(self, request):
        """ Create a new note (Only for logged-in users) """
        data = request.data
        course = get_object_or_404(Course, id=data["course_id"])

        new_note = Note.objects.create(
            name=data["name"],
            file_url=data["file_url"],
            course=course,
            user=request.user,
            tags=data.get("tags", ""),
        )

        return Response(
            {"note": {
                "id": new_note.id,
                "name": new_note.name,
                "file_url": new_note.file_url,
                "course_id": new_note.course.id,
                "tags": new_note.tags
            }},
            status=status.HTTP_201_CREATED
        )


class NoteDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """ Retrieve a single note (Only owner can view) """
        note = get_object_or_404(Note, id=pk)
        if note.user != request.user:
            return Response({"error": "You do not have permission to view this note."}, status=status.HTTP_403_FORBIDDEN)

        note_data = {
            "id": note.id,
            "name": note.name,
            "file_url": note.file_url,
            "course_id": note.course.id,
            "course_name": note.course.name,
            "user": note.user.username,
            "tags": note.tags,
            "created_at": note.created_at,
            "updated_at": note.updated_at,
        }
        return Response(note_data)

    def put(self, request, pk):
        """ Update a note (Only owner can update) """
        note = get_object_or_404(Note, id=pk)
        if note.user != request.user:
            return Response({"error": "You do not have permission to update this note."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        note.name = data.get("name", note.name)
        note.file_url = data.get("file_url", note.file_url)
        note.tags = data.get("tags", note.tags)

        if "course_id" in data:
            note.course = get_object_or_404(Course, id=data["course_id"])

        note.save()
        return Response({"message": "Note updated successfully!", "note": {
            "id": note.id,
            "name": note.name,
            "file_url": note.file_url,
            "course_id": note.course.id,
            "tags": note.tags
        }}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """ Delete a note (Only owner can delete) """
        note = get_object_or_404(Note, id=pk)
        if note.user != request.user:
            return Response({"error": "You do not have permission to delete this note."}, status=status.HTTP_403_FORBIDDEN)

        note.delete()
        return Response({"message": "Note deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


class NoteSearchView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """ Search notes (Only owner's notes) """
        query = request.GET.get("q", "")
        field = request.GET.get("field", "name")

        if not query:
            return Response({"error": "Missing query parameter 'q'"}, status=status.HTTP_400_BAD_REQUEST)

        allowed_fields = ["name", "tags", "course__name"]
        if field not in allowed_fields:
            return Response({"error": f"Invalid search field '{field}'"}, status=status.HTTP_400_BAD_REQUEST)

        filter_kwargs = {f"{field}__icontains": query}
        notes = Note.objects.filter(user=request.user).filter(**filter_kwargs)

        notes_data = [
            {
                "id": note.id,
                "name": note.name,
                "file_url": note.file_url,
                "course_id": note.course.id,
                "course_name": note.course.name,
                "user": note.user.username,
                "tags": note.tags,
                "created_at": note.created_at,
                "updated_at": note.updated_at,
            }
            for note in notes
        ]

        return Response({"results": notes_data})
