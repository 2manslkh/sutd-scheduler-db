from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ScheduleRequestForm, inputModuleInformation

# Create your views here.


@login_required
def index(request):
    if request.method == "POST":
        form = ScheduleRequestForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Request submitted')
            form.save()

    else:
        form = ScheduleRequestForm()
    return render(request, 'formstoadmin/index.html', {'form': form})


def inputModule(request):
    if request.method == "POST":
        module_form = inputModuleInformation(request.POST)
        if module_form.is_valid():
            messages.success(request, 'Request submitted')
            module_form.save()

    else:
        module_form = inputModuleInformation()
    return render(request, 'formstoadmin/index.html', {'form': module_form})


def addEvent(request):
    pass


def viewRequests(request):
    return render(request, 'formstoadmin/viewrequests.html')
