from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from django.http import JsonResponse
from django.core import serializers
from users.models import Module
from users.models import Class
from users.models import FilteredResults

import export_to_gcal

@login_required
def home(request):
    return render(request, 'schedule/home.html')


@login_required
def generateSchedule(request):
    if not request.user.profile.is_cc():
        messages.error(request, "Not authorized")
        redirect(request.path_info)

    if request.method == "POST":
        algo.run()
        messages.success(request, "Generating Schedule...")

    return render(request, 'schedule/generateSchedule.html')

def make_temp_model(data):
    FilteredResults.objects.all().delete()
    for i in data:
        a = FilteredResults(title=i["title"],start=i["start"],end=i["end"],description=i["description"],location=i["location"])
        a.save()

def return_data(request,Classs = "",modyews = ""):
    json_serializer = serializers.get_serializer("json")()
    # obj = json_serializer.serialize(Class.timetable_objects.all(), ensure_ascii=False)
    # out = open("testJSON1.json", "w")
    # out.write(obj)
    # out.close()
    if Classs == "" and modyews == "":
        data = list(Class.objects.values('title', 'start','end','description','location'))
    else:
        if Classs != "" and modyews == "":
            if Classs == "courses":
                data = list(Class.objects.values('title').distinct())
            else:
                data = []
                if "Class" in Classs:
                    classes = Classs.split(" ")
                    for i in classes:
                        if i != "Class":
                            qsetclass = Class.objects.filter(class_related__contains = i)
                            data.extend(list(qsetclass.values('title', 'start','end','description','location')))
                else:
                    courses = Classs.split("+")
                    for i in courses:
                        qsetcourse = Class.objects.filter(title__contains = i)
                        data.extend(list(qsetcourse.values('title', 'start','end','description','location')))
                    print("DATA: " + str(data))
                    make_temp_model(data)
                # else:
                #     qset1 = Class.objects.filter(class_related__contains = Classs)
                #     data = list(qset1.values('title', 'start','end','description','location'))
        else:
            courses = Classs.split()
            data = []
            for i in courses:
                qset = list((Class.objects.filter(title__contains = i)).values('title', 'start','end','description','location'))
                data.extend(qset)   

    # data = {
    #     'events': Module.timetable_objects.values('title', 'start','end','description','location')
    # }

    json_response = JsonResponse(data, safe=False)
    return json_response

@csrf_exempt
def export(request):
    export_to_gcal.main()
    return HttpResponse("OK")
