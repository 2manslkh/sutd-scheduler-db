from django import forms
import datetime


PREFERRED_TIMINGS = (
    ('morning', 'Morning'),
    ('earlyAfternoon', 'Early Afternoon'),
    ('lateAfternoon', 'Late Afternoon')
)


class ScheduleRequestForm(forms.Form):
    name = forms.CharField()
    course_code = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': "Enter the course code this request is relevant to"}))
    class_related = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 3, 'cols': 20, 'placeholder': "Input relevant classes separated by a comma. Eg. CC1, CC2. \n**This will be replaced by a multiple choice question with options that fetch from database"}))
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
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()
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
