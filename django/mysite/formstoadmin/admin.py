from django.contrib import admin
from .models import ScheduleRequest, EventRequest

# Register your models here.
admin.site.register(ScheduleRequest)
admin.site.register(EventRequest)
