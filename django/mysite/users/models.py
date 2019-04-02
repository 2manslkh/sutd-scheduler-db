from django.db import models
from django.contrib.auth.models import User

# # Create your models here.

class myUser(models.Model):
    REQUIRED_FIELDS = ('user',)
    user = models.OneToOneField(User, related_name='profile', unique=True, on_delete=models.CASCADE)
    access_level = models.IntegerField()

class Module(models.Model):
    title = models.CharField(max_length=200)
    class_type = models.CharField(max_length=200)
    class_related = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
    day = models.CharField(max_length=200)
    start = models.CharField(max_length=200)
    end = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    makeup = models.CharField(max_length=200)
    assigned_Professors = models.CharField(max_length=200)
    course_Lead = models.CharField(max_length=200)
    Cohort_Size = models.CharField(max_length=200)
    Enrolment_Size = models.CharField(max_length=200)