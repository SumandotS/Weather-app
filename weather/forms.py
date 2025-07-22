# forms.py
from django import forms

class CityForm(forms.Form):
    city = forms.CharField(label='Enter city name', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'e.g., Bengaluru'
    }))

class MapForm(forms.Form):
    KIND_CHOICES = [
        ('radar', 'Radar (Past + Future)'),
        ('satellite', 'Infrared Satellite')
    ]

    COLOR_SCHEME_CHOICES = [
        (0, 'Black and White Values'),
        (1, 'Original'),
        (2, 'Universal Blue'),
        (3, 'TITAN'),
        (4, 'The Weather Channel'),
        (5, 'Meteored'),
        (6, 'NEXRAD Level-III'),
        (7, 'RAINBOW @ SELEX-SI'),
        (8, 'Dark Sky')
    ]

    kind = forms.ChoiceField(choices=KIND_CHOICES, widget=forms.RadioSelect)
    color_scheme = forms.ChoiceField(choices=COLOR_SCHEME_CHOICES)