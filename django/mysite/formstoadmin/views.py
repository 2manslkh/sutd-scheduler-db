from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ScheduleRequestForm, inputModuleInformation, EventRequestForm
from django.contrib import messages
from .models import ScheduleRequest
# Create your views here.


@login_required
def index(request):
    if request.method == "POST":
        form = ScheduleRequestForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Request submitted')
            # form.save()

    else:
        form = ScheduleRequestForm()
    return render(request, 'formstoadmin/index.html', {'form': form})


@login_required
def inputModule(request):
    if request.method == "POST":
        module_form = inputModuleInformation(request.POST)
        if module_form.is_valid():
            messages.success(request, 'Input module form submitted')
            # module_form.save()

    else:
        module_form = inputModuleInformation()
    return render(request, 'formstoadmin/index.html', {'form': module_form})


@login_required
def addEvent(request):
    if request.method == "POST":
        form = EventRequestForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Event Scheduling form submitted')
            # form.save()

    else:
        form = EventRequestForm()
    return render(request, 'formstoadmin/index.html', {'form': form})


@login_required
def viewRequests(request):
    query_results = ScheduleRequest.objects.all()
    fields = ScheduleRequest._meta.get_fields()
    return render(request, 'formstoadmin/viewrequests.html')
