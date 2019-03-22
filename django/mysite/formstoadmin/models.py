from django.db import models
from multiselectfield import MultiSelectField

PREFERRED_TIMINGS = (
    ('morning', 'Morning'),
    ('earlyAfternoon', 'Early Afternoon'),
    ('lateAfternoon', 'Late Afternoon')
)


class ScheduleRequest(models.Model):
    name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=200)
    class_related = models.CharField(max_length=200)
    preferred_timings = MultiSelectField(choices=PREFERRED_TIMINGS)
    reasons = models.CharField(max_length=200)
    remarks = models.CharField(max_length=200)
