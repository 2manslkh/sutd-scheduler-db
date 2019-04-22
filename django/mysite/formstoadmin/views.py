from django.shortcuts import render, redirect
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
        form = ScheduleRequestForm(request.POST, initial={'name': request.user.get_username()})
        if form.is_valid():
            messages.success(request, 'Request submitted')

            # def save(self):
            data = form.cleaned_data
            s = ScheduleRequest(
                name=request.user.get_username(),
                course_code=data['course_code'],
                class_related=data['class_related'],
                preferred_timings=data['preferred_timings'],
                reasons=data['reasons'],
                remarks=data['remarks']
            )
            s.save()
            form = ScheduleRequestForm(initial={'name': request.user.get_username()})
    else:
        form = ScheduleRequestForm(initial={'name': request.user.get_username()})  # or use user.get_username() for username
    return render(request, 'formstoadmin/schedulerequest.html', {'form': form})


@login_required
def inputModule(request):
    if request.method == "POST":
        module_form = InputModuleInformation(request.POST)
        if module_form.is_valid():
            data = module_form.cleaned_data
            _, created = Module.objects.filter(subject__iexact=data['subject']).update_or_create(
                subject__iexact=data['subject'],
                code=data['subject_code'],
                defaults={
                    'pillar': data['pillar'],
                    'term': data['term'],
                    'core': data['core'],
                    'subject_lead': data['subject_lead'],
                    'cohort_size': data['cohort_size'],
                    'cohorts': data['cohorts'],
                    'enrolment_size': data['enrolment_size'],
                    'cohorts_per_week': data['cohorts_per_week'],
                    'lectures_per_week': data['lectures_per_week'],
                    'labs_per_week': data['labs_per_week']
                })
            module_form = InputModuleInformation()
            if created == False:
                messages.success(request, 'Updated module')
            else:
                messages. success(request, 'Added module')
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
                form.save()
                form = InputClassInformation()
                messages.success(request, 'Class information added')

        return render(request, self.template_name, {'form': form})


def inputClassInfo_start(request):
    form = InputClassInformation()
    if request.method == "POST":
        print("hi")
        print(request.POST.get("module", ""))
    return render(request, 'formstoadmin/inputclass.html', {'form': form, 'start': True})


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
    all_requests = ScheduleRequest.objects.all()
    if request.method == "GET":
        query_results = ScheduleRequest.objects.filter(approved__isnull=True)
        fields = ScheduleRequest._meta.get_fields()
        return render(request, 'formstoadmin/viewrequests.html', {"query_results": query_results, "all_requests": all_requests})


def request_action(request, requestID, status):
    query_results = ScheduleRequest.objects.filter(approved__isnull=True)
    all_requests = ScheduleRequest.objects.all()
    fields = ScheduleRequest._meta.get_fields()
    if status == 0:
        stat = True
    elif status == 1:
        stat = False

    a = all_requests[requestID - 1]
    a.approved = stat
    a.save()

    return redirect('/view-requests')


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

        header = True
        for row in csv.reader(io_string, delimiter=','):
            if header:
                if len(row) != 12:
                    raise IndexError
                header = False

            else:
                _, created = Module.objects.update_or_create(
                    subject=row[0],
                    pillar=row[1],
                    defaults={
                        'code': row[2],
                        'term': row[3],
                        'core': row[4],
                        'subject_lead': row[5],
                        'cohort_size': row[6],
                        'cohorts': row[7],
                        'enrolment_size': row[8],
                        'cohorts_per_week': row[9],
                        'lectures_per_week': row[10],
                        'labs_per_week': row[11]
                    })
    except IndexError:
        messages.error(request, "Incorrect number of columns. Please ensure data is in the right format")
        return render(request, template, context)

    data = pd.read_csv(csv_file2)
    data_html = data.to_html(classes='table', justify="left", border=0)
    context = {'loaded_data': data_html}

    messages.success(request, 'File uploaded')
    return render(request, template, context)
