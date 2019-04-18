from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ScheduleRequestForm, inputModuleInformation, EventRequestForm
from django.contrib import messages
from .models import ScheduleRequest
from django.core import serializers
from django.contrib.auth.models import User
# Create your views here.

import csv
import io
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from users.models import Module


@login_required
def index(request):
    if request.method == "POST":
        form = ScheduleRequestForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Request submitted')

            # def save(self):
            data = form.cleaned_data
            s = ScheduleRequest(
                name=data['name'],
                course_code=data['course_code'],
                class_related=data['class_related'],
                preferred_timings=data['preferred_timings'],
                reasons=data['reasons'],
                remarks=data['remarks']
            )
            s.save()
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
    return render(request, 'formstoadmin/inputmodule.html', {'form': module_form})


@login_required
def addEvent(request):
    if request.method == "POST":
        form = EventRequestForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Event Scheduling form submitted')
            # form.save()

    else:
        form = EventRequestForm()
    return render(request, 'formstoadmin/addevent.html', {'form': form})


@login_required
def viewRequests(request):
    query_results = ScheduleRequest.objects.all()
    fields = ScheduleRequest._meta.get_fields()
    return render(request, 'formstoadmin/viewrequests.html', {"query_results": query_results})


def generate_courses(request):
    json_serializer = serializers.get_serializer("json")()
    data = list(User.objects.values('username'))
    return JsonResponse(data, safe=False)


@permission_required('admin.can_add_log_entry')
def moduleUpload(request):
    template = "formstoadmin/test.html"
    prompt = {
        'order': "Order of csv should be Subject, Code, Term, Core, Subject_Lead, Cohort_Size, Cohorts, Enrolment_Size, Cohorts Per Week, Lectures Per Week, Labs Per Week"
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, "This file is not a .csv file")

    data_set = csv_file.read().decode('utf-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Module.objects.update_or_create(
            subject=column[0],
            code=column[1],
            term=column[2],
            core=column[3],
            subject_lead=column[4],
            cohort_size=column[5],
            enrolment_size=column[6],
            cohorts_per_week=column[7],
            lectures_per_week=column[8],
            labs_per_week=column[9],
        )

    context = {}
    return render(request, template, context)
