from django.db import models

# ✅ Course Model (No Year/Term Here!)
class Course(models.Model):
    id = models.CharField(max_length=20, primary_key=True)  
    name = models.CharField(max_length=255)  

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return f"{self.id} - {self.name}"