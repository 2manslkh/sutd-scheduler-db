from django import forms
import datetime
from django_select2.forms import ModelSelect2Widget
from schedule.models import Module, Class
PREFERRED_TIMINGS = (
    ('morning', 'Morning'),
    ('earlyAfternoon', 'Early Afternoon'),
    ('lateAfternoon', 'Late Afternoon')
)

# useful form fields
'''
help_text=""
'''


class ScheduleRequestForm(forms.Form):
    name = forms.CharField(disabled=True, initial="Sudipta Chattopadhyay")
    # course_code = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': "Enter the course code this request is relevant to"}))
    course_code = forms.ModelChoiceField(
        queryset=Module.objects.all(),
        label="course_code",
        widget=ModelSelect2Widget(
            model=Module,
            search_fields=['name__icontains'],
        )
    )

    class_related = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        label="class_related",
        widget=ModelSelect2Widget(
            model=Class,
            search_fields=['name__icontains'],
            dependent_fields={'course_code': 'course_code'},
        )
    )

    # class_related = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 3, 'cols': 20, 'placeholder': "Input relevant classes separated by a comma. Eg. CC1, CC2. \n**This will be replaced by a multiple choice question with options that fetch from database"}))
    preferred_timings = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=PREFERRED_TIMINGS)
    reasons = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 20}))
    remarks = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3, 'cols': 20}))


PILLARS = (
    ('asd', 'ASD'),
    ('epd', 'EPD'),
    ('esd', 'ESD'),
    ('istd', 'ISTD'),
    ('hass', 'HASS'),
)


class EventRequestForm(forms.Form):
    persons_in_charge = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': "Separate names by commas"}))
    event_name = forms.CharField()
    relevant_pillars = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=PILLARS)
    start_date = forms.DateTimeField(input_formats=['%d/%m/%y'], help_text="DD/MM/YYYY")
    start_time = forms.DateTimeField(input_formats=['%H:%M'], help_text="HH:MM eg. 14:30")
    end_date = forms.DateTimeField(input_formats=['%d/%m/%y'], help_text="DD/MM/YYYY")
    end_time = forms.DateTimeField(input_formats=['%H:%M'], help_text="HH:MM eg. 16:30")
    duration = forms.DurationField()


LOCATION_TYPE = (
    ('LT', "Lecture Theatre"),
    ('Cohort', "Cohort classroom"),
)


# TODO: FOR RELEVANT FIELDS, SEARCH FROM DATABASE ONCE FIELDS ARE BEING FILLED
class inputModuleInformation(forms.Form):
    module_name = forms.CharField()
    location_type = forms.ChoiceField(choices=LOCATION_TYPE)
    location = forms.CharField()
    duration = forms.IntegerField()

    # TODO: implement multiple date picker
    # https://tempusdominus.github.io/bootstrap-4/
    makeup = forms.DateTimeField()

    # TODO: Press 'Tab' when half of the answers are typed
    # list of all classes attending this timeslot
    class_related = forms.CharField()
    assigned_professors = forms.CharField()

    # TODO: automatically generate the following when module is selected
    course_lead = forms.CharField()
    cohort_size = forms.IntegerField()
    enrolment_size = forms.IntegerField()
