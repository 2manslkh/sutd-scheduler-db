from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from .forms import ScheduleRequestForm, InputModuleInformation, EventRequestForm, InputClassInformation
from django.contrib import messages
from .models import ScheduleRequest, EventRequest
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
                course_name=data['course_name'],
                duration=data['duration'],
                class_related=data['class_related'],
                lesson_type=data['lesson_type'],
                preferred_timings=data['preferred_timings'],
                reasons=data['reasons'],
                remarks=data['remarks'],
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
                    'subject': data['subject'],
                    'code': data['subject_code'],
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
            print(created)
            if created == False:
                messages.success(request, 'Updated module')
            else:
                messages. success(request, 'Added module')
    else:
        module_form = InputModuleInformation()
    return render(request, 'formstoadmin/inputmodule.html', {'form': module_form})


def inputClassInfo(request, mod_id=0, idx=0, step=0):
    module = Module.objects.filter(id=mod_id)[0].subject
    try:
        classes = Class.objects.filter(module__subject=module)
        end_idx = len(classes) - 1
    except:
        messages.error(request, "There are no classes under this module!")
        return redirect("/input-class-info-start/")

    if step == 1 and idx != 0:
        idx -= 1
    elif step == 2 and idx != end_idx:
        idx += 1

    try:
        current_class = classes[int(idx)]
        print(current_class)
    except:
        messages.error(request, "Somehow you accessed a non-existent class!")
        return redirect("/input-class-info-start/")

    if request.method == "POST":
        form = InputClassInformation(request.POST)
        form.module = module
        if form.is_valid():
            form = InputClassInformation(request.POST, instance=current_class)
            form.save()
            messages.success(request, 'Class information updated')
            form = InputClassInformation(instance=current_class)

    else:
        # for c in classes:
        #     print(c.id, c.module)
        form = InputClassInformation(instance=current_class)

    context = {'form': form, 'mod_id': mod_id, 'end_idx': end_idx, 'idx': idx, 'step': step}

    return render(request, "formstoadmin/inputclass.html", context)


def inputClassInfo_start(request):
    form = InputClassInformation()
    if request.method == "POST":
        mod_id = request.POST.get("module", "")
        urlstr = f"/input-class-info/{mod_id}/0/0"
        return redirect(urlstr)

    return render(request, 'formstoadmin/inputclass.html', {'form': form, 'start': True})


@login_required
def addEvent(request):
    if request.method == "POST":
        form = EventRequestForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            e = EventRequest(
                persons_in_charge=data['persons_in_charge'],
                event_name=data['event_name'],
                relevant_pillars=data['relevant_pillars'],
                date=data['date'],
                duration=data['duration'],
                num_people=data['num_people'],
            )
            e.save()
            # messages.success(request, 'Event Schedule form submitted')
            form = EventRequestForm()

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
