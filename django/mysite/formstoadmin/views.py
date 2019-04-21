from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import ScheduleRequestForm, InputModuleInformation, EventRequestForm, InputClassInformation
from django.contrib import messages
from .models import ScheduleRequest
from django.core import serializers
from django.contrib.auth.models import User
import pandas as pd
import copy
from django.views.generic import FormView
# Create your views here.

import csv
import io
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from users.models import Module, Class


@login_required
def scheduleRequest(request):
    if request.method == "POST":
        form = ScheduleRequestForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Request submitted')

            # def save(self):
            data = form.cleaned_data
            s = ScheduleRequest(
                name=request.user.get_full_name(),
                course_code=data['course_code'],
                class_related=data['class_related'],
                preferred_timings=data['preferred_timings'],
                reasons=data['reasons'],
                remarks=data['remarks']
            )
            s.save()
            form = ScheduleRequestForm()
    else:
        form = ScheduleRequestForm(initial={'name': request.user.get_full_name()})  # or use user.get_username() for username
    return render(request, 'formstoadmin/schedulerequest.html', {'form': form})


@login_required
def inputModule(request):
    if request.method == "POST":
        module_form = InputModuleInformation(request.POST)
        if module_form.is_valid():
            messages.success(request, 'Input module form submitted')
            data = module_form.cleaned_data
            s = Module(
                subject=data['subject'],
                code=data['subject_code'],
                pillar=data['pillar'],
                term=data['term'],
                core=data['core'],
                subject_lead=data['subject_lead'],
                cohort_size=data['cohort_size'],
                enrolment_size=data['enrolment_size'],
                cohorts=data['cohorts'],
                cohorts_per_week=data['cohorts_per_week'],
                lectures_per_week=data['lectures_per_week'],
                labs_per_week=data['labs_per_week'],
            )
            s.save()
            module_form = InputModuleInformation()
    else:
        module_form = InputModuleInformation()
    return render(request, 'formstoadmin/inputmodule.html', {'form': module_form})


class InputClassInfo(FormView):
    template_name = "formstoadmin/inputclass.html"

    def get(self, request):
        form = InputClassInformation()
        classes = Class.objects.all()
        context = {'form': form, 'classes': classes}
        return render(request, self.template_name, context)

    def post(self, request):
        form = InputClassInformation(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            subject = data['module']
            if Class.objects.filter(module__subject=subject).exists():
                a = Class.objects.filter(module__subject=subject)[0]
                form = InputClassInformation(request.POST, instance=a)
                form.save()
                messages.success(request, 'Class information updated')

            else:
                f.save()
                form = InputClassInformation()
                messages.success(request, 'Class information added')

        return render(request, self.template_name, {'form': form})


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
def viewRequests(request, approved=''):
    if request.method == "GET":
        query_results = ScheduleRequest.objects.all()
        fields = ScheduleRequest._meta.get_fields()
        return render(request, 'formstoadmin/viewrequests.html', {"query_results": query_results})


def request_action(request, requestID, status):
    if request.method == "GET":
        query_results = ScheduleRequest.objects.all()
        fields = ScheduleRequest._meta.get_fields()
        return render(request, 'formstoadmin/viewrequests.html', {"query_results": query_results})


def generate_courses(request):
    json_serializer = serializers.get_serializer("json")()
    data = list(User.objects.values('username'))
    return JsonResponse(data, safe=False)


@permission_required('admin.can_add_log_entry')
def moduleUpload(request):
    template = "formstoadmin/moduleupload.html"
    context = {'loaded_data': None}

    if request.method == "GET":
        return render(request, template)

    csv_file = request.FILES['file']
    csv_file2 = copy.deepcopy(csv_file)

    if not csv_file.name.endswith('.csv'):
        messages.error(request, "Please upload a CSV file")
        return render(request, template, context)

    try:
        data_set = csv_file.read().decode('utf-8')
        io_string = io.StringIO(data_set)

        first_row = True
        for row in csv.reader(io_string, delimiter=',', quotechar="|"):
            if first_row:
                if len(row) != 12:
                    raise IndexError
                first_row = False

            else:
                _, created = Module.objects.update_or_create(
                    subject=row[0],
                    pillar=row[1],
                    code=row[2],
                    term=row[3],
                    core=row[4],
                    subject_lead=row[5],
                    cohort_size=row[6],
                    cohorts=row[7],
                    enrolment_size=row[8],
                    cohorts_per_week=row[9],
                    lectures_per_week=row[10],
                    labs_per_week=row[11]
                )
    except IndexError:
        messages.error(request, "Incorrect number of columns. Please ensure data is in the right format")
        return render(request, template, context)

    data = pd.read_csv(csv_file2)
    data_html = data.to_html(classes='table', justify="left", border=0)
    context = {'loaded_data': data_html}

    messages.success(request, 'File uploaded')
    return render(request, template, context)
