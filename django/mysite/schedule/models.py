from django.db import models

# Create your models here.
class Module(models.Model):
    name = models.CharField(max_length=200)
    class_type = models.CharField(max_length=200)
    class_related = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
    others = models.CharField(max_length=200)
    makeup = models.CharField(max_length=200)
    assigned_Professors = models.CharField(max_length=200)
    course_Lead = models.CharField(max_length=200)
    Cohort_Size = models.CharField(max_length=200)
    Enrolment_Size = models.CharField(max_length=200)
    
