from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


@login_required
def home(request):
    return render(request, 'schedule/home.html')


@login_required
def generateSchedule(request):
    if request.method == "POST":
        messages.success(request, "Generating Schedule...")

    return render(request, 'schedule/generateSchedule.html')
