from django.db import models
from django.contrib.auth.models import User

# # Create your models here.

class myUser(models.Model):
    REQUIRED_FIELDS = ('user',)
    user = models.OneToOneField(User, related_name='profile', unique=True, on_delete=models.CASCADE)
    access_level = models.IntegerField()

class Module(models.Model):
    subject = models.CharField(max_length = 200)
    code = models.CharField(max_length=200)
    term = models.CharField(max_length=200)
    core = models.CharField(max_length = 200)
    subject_lead = models.CharField(max_length=200)
    cohort_size = models.CharField(max_length=200)
    enrolment_size = models.CharField(max_length=200)    

    all_title = models.CharField(max_length = 200)
    all_type = models.CharField(max_length=200)
    all_class_related =  models.CharField(max_length=200)
    all_location = models.CharField(max_length=200)
    all_duration =models.CharField(max_length = 200)
    all_start = models.CharField(max_length = 200)
    all_end = models.CharField(max_length = 200)
    all_others = models.CharField(max_length = 200)
    all_makeup = models.CharField(max_length = 200)
    all_assigned_Professors = models.CharField(max_length = 200)

class Class(models.Model):
    title = models.ForeignKey(Module,on_delete=models.CASCADE,related_name="title")
    class_type =models.ForeignKey(Module,on_delete=models.CASCADE,related_name="class_type") 
    class_related =models.ForeignKey(Module,on_delete=models.CASCADE,related_name="class_related")
    location = models.ForeignKey(Module,on_delete=models.CASCADE,related_name="location")
    duration =  models.ForeignKey(Module,on_delete=models.CASCADE,related_name="duration")
    start = models.ForeignKey(Module,on_delete=models.CASCADE,related_name="start")
    end = models.ForeignKey(Module,on_delete=models.CASCADE,related_name="end")
    assigned_Professors = models.ForeignKey(Module,on_delete=models.CASCADE,related_name="others")
    others = models.ForeignKey(Module,on_delete=models.CASCADE,related_name="makeup")
    makeup =  models.ForeignKey(Module,on_delete=models.CASCADE,related_name="assigned_Professors")