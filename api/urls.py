from django.urls import path
from .views import (
    GoogleLoginView,
    SearchNotesView,
    CurriculumCoursesView,
    CourseListView,
    NoteListCreateView,
    NoteDetailView,
    NoteSearchView,
    GetTokenByEmailView,
    CourseDetailView,
)




urlpatterns = [
    path('auth/google/', GoogleLoginView.as_view(), name='google-login'),
    path("auth/token", GetTokenByEmailView.as_view(), name="get-token"),
    
    # 🎯 Course API
    path("courses/", CourseListView.as_view(), name="course-list"),  # GET all courses, POST new course
    path("courses/<str:course_id>/", CourseDetailView.as_view(), name="course-detail"),  # GET, PUT, DELETE specific course
    path('curriculum/', CurriculumCoursesView.as_view(), name='curriculum-latest'),  # Get latest curriculum courses

    # 🎯 Note APIs
    path("notes/", NoteListCreateView.as_view(), name="note-list-create"),  # List & Create
    path("notes/<int:pk>/", NoteDetailView.as_view(), name="note-detail"),  # Retrieve, Update, Delete
    path('notes/search/', SearchNotesView.as_view(), name='search-notes'),
]





