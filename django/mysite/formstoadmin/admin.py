from django.contrib import admin
from .models import ScheduleRequest, EventRequest, EventRequestResponse

# Register your models here.
admin.site.register(ScheduleRequest)
admin.site.register(EventRequest)
admin.site.register(EventRequestResponse)
