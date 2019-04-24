from django.db import models
from multiselectfield import MultiSelectField

PREFERRED_TIMINGS = (
    ('Morning', 'Morning'),
    ('Afternoon', 'Afternoon'),
)

PILLARS = (

    ('asd', 'ASD'),
    ('epd', 'EPD'),
    ('esd', 'ESD'),
    ('istd', 'ISTD'),
    ('hass', 'HASS'),
)


class ScheduleRequest(models.Model):
    name = models.CharField(max_length=200,default="")
    course_name = models.CharField(max_length=200,default="")
    class_related = models.CharField(max_length=200,default="")
    duration = models.CharField(max_length=200,default="")
    lesson_type = models.CharField(max_length=200,default="")
    preferred_timings = MultiSelectField(choices=PREFERRED_TIMINGS)
    reasons = models.CharField(max_length=200,default="")
    remarks = models.CharField(max_length=200,default="")
    approved = models.BooleanField(null=True)


class EventRequest(models.Model):
    event_id = models.CharField(max_length=200,default="")
    persons_in_charge = models.CharField(max_length=200,default="")
    event_name = models.CharField(max_length=200,default="")
    relevant_pillars = MultiSelectField(choices=PILLARS)
    date = models.CharField(max_length=200,default="")
    duration = models.CharField(max_length=200,default="")
    num_people = models.CharField(max_length=200,default="")
    start_time = models.CharField(max_length=200,default="")
    end_time = models.CharField(max_length=200,default="")
    location = models.CharField(max_length=200,default="")
    submitted_by = models.CharField(max_length=200,default="")


class EventRequestResponse(models.Model):
    event_id = models.ForeignKey(EventRequest, on_delete=models.CASCADE, default="")
    persons_in_charge = models.CharField(max_length=200,default="")
    event_name = models.CharField(max_length=200,default="")
    relevant_pillars = MultiSelectField(choices=PILLARS)
    date = models.CharField(max_length=200,default="")
    duration = models.CharField(max_length=200,default="")
    num_people = models.CharField(max_length=200,default="")
    start_time = models.CharField(max_length=200,default="")
    end_time = models.CharField(max_length=200,default="")
    location = models.CharField(max_length=200,default="")
    submitted_by = models.CharField(max_length=200,default="")
