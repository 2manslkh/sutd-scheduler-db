from django import forms
import datetime
from users.models import Module, Class

PREFERRED_TIMINGS = (
    ('morning', 'Morning'),
    ('afternoon', 'Afternoon'),
)

LESSON_TYPE = (
    ('Lecture', 'Lecture'),
    ('Cohort Class', 'Cohort Class'),
)

LOCATION_TYPE = (
    ('LT', "Lecture Theatre"),
    ('Cohort', "Cohort classroom"),
)

CLASSES = (
    ('Lab', "Lab"),
    ('Cohort Class', "Cohort Class"),
    ('Lecture', "Lecture"),
)

PILLARS = (
    ('ASD', 'ASD'),
    ('EPD', 'EPD'),
    ('ESD', 'ESD'),
    ('ISTD', 'ISTD'),
    ('HASS', 'HASS'),
)


class ScheduleRequestForm(forms.Form):
    name = forms.CharField(disabled=True, required=False)
    course_name = forms.ModelChoiceField(queryset=Module.objects.all().order_by('subject').distinct())
    duration = forms.IntegerField(label="Duration (in hours)", min_value=1)
    lesson_type = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LESSON_TYPE)
    class_related = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 2, 'cols': 20, 'placeholder': "Input relevant classes separated by a comma. Eg. 5CISTD01, 5CISTD02."}))
    preferred_timings = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=PREFERRED_TIMINGS)
    reasons = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 20}))
    remarks = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3, 'cols': 20}))


class EventRequestForm(forms.Form):
    persons_in_charge = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': "Separate names by commas"}))
    event_name = forms.CharField()
    relevant_pillars = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=PILLARS)
    date = forms.DateTimeField(input_formats=['%d/%m/%y'], help_text="DD/MM/YYYY. Suggested timeslots will be given around the date provided")
    duration = forms.IntegerField(label="Duration (in hours)", min_value=1)


class InputModuleInformation(forms.Form):
    class Meta:
        model = Module
        fields = "__all__"
    subject = forms.CharField()  # $, disabled=True)
    pillar = forms.ChoiceField(choices=PILLARS)
    subject_code = forms.CharField()
    term = forms.IntegerField(min_value=1, max_value=10)
    core = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'placeholder': "True/False"}))
    subject_lead = forms.CharField(help_text="Please separate professors\' names with a comma")
    cohort_size = forms.IntegerField(min_value=1)
    cohorts = forms.IntegerField(min_value=1, label="Number of Cohort Classes")
    enrolment_size = forms.IntegerField(min_value=1)
    cohorts_per_week = forms.IntegerField(min_value=0)
    lectures_per_week = forms.IntegerField(required=False, min_value=0)
    labs_per_week = forms.IntegerField(required=False, min_value=0)


class InputClassInformation(forms.ModelForm):
    class Meta:
        model = Class
        fields = '__all__'

    module = forms.ModelChoiceField(queryset=Module.objects.all().order_by('subject').distinct())
    title = forms.CharField(disabled=True, required=False)
    pillar = forms.CharField(disabled=True, required=False)
    Type = forms.CharField(disabled=True, required=False)
    class_related = forms.CharField(disabled=True, required=False)
    location = forms.CharField()
    duration = forms.CharField(disabled=True, required=False)
    start = forms.CharField(disabled=True, required=False)
    end = forms.CharField(disabled=True, required=False)
    description = forms.CharField()
    makeup = forms.CharField()
    assigned_professors = forms.CharField(help_text="Please separate professors\' names with a comma")
    day = forms.CharField(disabled=True, required=False)

    def __init__(self, *args, **kwargs):
        super(InputClassInformation, self).__init__(*args, **kwargs)
        self.fields['module'].widget.attrs['class'] = 'choose-mod'


# useful queries
'''
Class.objects.filter(module__subject="Documentary")

queryset = Class.objects.all()
for query in queryset:
    print (query.module)
    print (query.title)
'''
