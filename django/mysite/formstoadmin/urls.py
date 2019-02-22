from django.urls import path
from . import views

urlpatterns = [
    # '' contains string after /requestform
    path('', views.index, name='request-form'),
]
