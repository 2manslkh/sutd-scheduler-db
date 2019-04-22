from django.db import models
from django.contrib.auth.models import User

# # Create your models here.

class myUser(models.Model):
    REQUIRED_FIELDS = ('user',)
    user = models.OneToOneField(User, related_name='profile', unique=True, on_delete=models.CASCADE)
    access_level = models.IntegerField()

class Module(models.Model):
    subject = models.CharField(max_length=200, default="")
    pillar = models.CharField(max_length=200, default="")
    code = models.CharField(max_length=200, default="")
    term = models.CharField(max_length=200, default="")
    core = models.CharField(max_length =200, default="")
    subject_lead = models.CharField(max_length=200, default="")
    cohort_size = models.CharField(max_length=200, default="")
    cohorts = models.CharField(max_length=200, default="")
    enrolment_size = models.CharField(max_length=200, default="")    
    cohorts_per_week = models.CharField(max_length=200, default="")
    lectures_per_week = models.CharField(max_length=200, default="")
    labs_per_week = models.CharField(max_length=200, default="")


class Class(models.Model):
    module = models.ForeignKey(Module,on_delete=models.CASCADE,default="")
    title = models.CharField(max_length=200, default = "")
    pillar = models.CharField(max_length=200, default="")
    type = models.CharField(max_length=200, default = "")
    class_related =  models.CharField(max_length=200, default = "")
    location = models.CharField(max_length=200, default = "")
    duration =models.CharField(max_length=200, default = "")
    assigned_professors =models.CharField(max_length=200, default = "")
    description= models.CharField(max_length=200, default = "")
    makeup = models.CharField(max_length=200, default = "")
    day = models.CharField(max_length=200, default = "")
    start = models.CharField(max_length=200, default = "")
    end = models.CharField(max_length=200, default = "")
 