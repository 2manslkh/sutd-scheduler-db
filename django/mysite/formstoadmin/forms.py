from django import forms

PREFERRED_TIMINGS = (
    ('nil', 'No preferred timings'),
    ('morning', 'Morning'),
    ('earlyAfternoon', 'Early Afternoon'),
    ('lateAfternoon', 'Late Afternoon')
)

TITLE = (
    ('nil', 'Select your title'),
    ('faculty', 'Faculty'),
    ('staff', 'Staff'),
    ('student', 'Student')
)

FORM_TYPE = (
    ('nil', 'Select your form type'),
    ("acad", "Academic Schedule Request"),
    ("event", "In-vivo event")
)


class RequestForm(forms.Form):
    form_type = forms.ChoiceField(choices=FORM_TYPE)
    title = forms.ChoiceField(choices=TITLE)
    preferred_timings = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=PREFERRED_TIMINGS)
    reasons = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 20, 'placeholder': "N.A. if not applicable"}))
    remarks = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3, 'cols': 20}))


# class EventRequestForm(forms.Form):
#     pass
# class ScheduleRequestForm(forms.Form):
