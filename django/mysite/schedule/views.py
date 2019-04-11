from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def home(request):
    return render(request, 'schedule/home.html')


@login_required
def generateSchedule(request):
    return render(request, 'schedule/generateSchedule.html')
