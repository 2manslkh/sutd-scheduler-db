from django.urls import path
from . import views

urlpatterns = [
    # '' contains string after /requestform
    path('', views.index, name='request-form'),
    path('input-module-info', views.inputModule, name='input-module-info'),
]
