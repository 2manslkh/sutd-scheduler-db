from django.urls import path
from . import views

urlpatterns = [
    #     # '' contains string after /requestform
    path('return_courses', views.generate_courses),
    path('<int:requestID>/<int:status>/', views.request_action),
]
