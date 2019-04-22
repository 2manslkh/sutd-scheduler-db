from django.urls import path
from . import views

urlpatterns = [
    #     # '' contains string after /requestform
    path('return_courses', views.generate_courses),
    path('<int:requestID>/<int:status>/', views.request_action),
    #     path('', views.index, name='request-form'),
    #     path('input-module-info', views.inputModule, name='input-module-info'),
    #     path('view-requests', views.viewRequests, name='view-requests'),
    #     path('add-event', views.addEvent, name='add-event'),
]
