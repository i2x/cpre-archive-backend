from django.db import models
from .course import Course

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