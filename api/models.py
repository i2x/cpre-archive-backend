from django.db import models
from django.contrib.auth.models import AbstractUser

# ✅ Custom User Model (Extends AbstractUser)
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('guest', 'Guest'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.username} ({self.role})"


# ✅ Curriculum Model
class Curriculum(models.Model):
    id = models.CharField(max_length=20, primary_key=True)  
    name = models.CharField(max_length=255)  
    year = models.IntegerField()  # Year when the course is taught


    class Meta:
        verbose_name = "Curriculum"
        verbose_name_plural = "Curriculums"

    def __str__(self):
        return f"{self.id} - {self.name}"


# ✅ Course Model (No Year/Term Here!)
class Course(models.Model):
    id = models.CharField(max_length=20, primary_key=True)  
    name = models.CharField(max_length=255)  

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return f"{self.id} - {self.name}"


# ✅ Curriculum-Course Mapping Model (Many-to-Many with Year & Term)
class CurriculumMapping(models.Model):  
    curriculum = models.ForeignKey(
        Curriculum, 
        on_delete=models.CASCADE, 
        related_name="courses"
    )  
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name="curriculums"
    )
    year = models.IntegerField()  # Year when the course is taught
    term = models.IntegerField()  # Term when the course is taught

    class Meta:
        verbose_name = "Curriculum Mapping"
        verbose_name_plural = "Curriculum Mappings"
        unique_together = ('curriculum', 'course', 'year', 'term')  # Prevent duplicate mappings

    def __str__(self):
        return f"{self.curriculum.name} - {self.course.name} (Year {self.year}, Term {self.term})"


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
