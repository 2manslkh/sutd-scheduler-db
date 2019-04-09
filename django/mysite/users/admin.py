from django.contrib import admin
from .models import Module, myUser, Class
# Register your models here.
 
admin.site.register(Module)
admin.site.register(Class)
admin.site.register(myUser)