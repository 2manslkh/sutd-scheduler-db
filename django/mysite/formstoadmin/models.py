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
    name = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    class_related = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
    lesson_type = models.CharField(max_length=200)
    preferred_timings = MultiSelectField(choices=PREFERRED_TIMINGS)
    reasons = models.CharField(max_length=200)
    remarks = models.CharField(max_length=200)
    approved = models.BooleanField(null=True)


class EventRequest(models.Model):
    persons_in_charge = models.CharField(max_length=200)
    event_name = models.CharField(max_length=200)
    relevant_pillars = MultiSelectField(choices=PILLARS)
    date = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
    num_people = models.CharField(max_length=200)
    start_time = models.CharField(max_length=200)
    end_time = models.CharField(max_length=200)
