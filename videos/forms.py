from django import forms


DEVICE_TYPES = (
    ('1', 'Mobile'),
    ('2', 'Tablet'),
    ('3', 'PC/Laptop'),
)

QUALITY_LIST = (
    ('1', '240p'),
    ('2', '360p'),
    ('3', '720p'),
)


class SurveyForm(forms.Form):
    device_type = forms.ChoiceField(choices=DEVICE_TYPES)
    quality = forms.ChoiceField(choices=QUALITY_LIST)
