from django.db import models
from .user import CustomUser
from .course import Course

# ✅ Note Model (No Real File, Uses URL + Tags for Searching)
class Note(models.Model):  
    name = models.CharField(max_length=255)  # Note title
    file_url = models.URLField()  # URL where the file is stored (Google Drive, S3, etc.)
    user = models.ForeignKey(
        CustomUser,  # ✅ Use CustomUser instead of default User model
        on_delete=models.CASCADE,
        related_name="notes"
    )  
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name="notes"
    )  
    thumbnail_url = models.URLField(blank=True, null=True)  # Thumbnail for preview
    tags = models.CharField(max_length=255, blank=True, null=True)  # Searchable tags (comma-separated)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    class Meta:
        verbose_name = "Course Note"
        verbose_name_plural = "Course Notes"

    def __str__(self):
        return f"{self.name} (Owned by: {self.user.username})"

    # 🔎 Search function: Find notes by name or tags
    @classmethod
    def search_notes(cls, query):
        return cls.objects.filter(models.Q(name__icontains=query) | models.Q(tags__icontains=query))