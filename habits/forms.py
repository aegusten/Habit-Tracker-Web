# forms.py

from django import forms
from .models import Habit

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'timeline', 'motivational_reminder', 'insights_method']


class HabitRecordForm(forms.Form):
    def __init__(self, *args, metrics=None, **kwargs):
        super().__init__(*args, **kwargs)
        if metrics:
            for key, info in metrics.items():
                imp = info.get('importance', 'daily_optional')
                if imp in ['daily_required', 'daily_optional']:
                    field_type = info.get('type', 'text')
                    label = info.get('label', key.replace('_', ' ').title())
                    required = (imp == 'daily_required')
                    if field_type == 'number':
                        self.fields[key] = forms.FloatField(label=label, required=required)
                    elif field_type == 'date':
                        self.fields[key] = forms.DateField(label=label, required=required,
                                              widget=forms.DateInput(attrs={'type': 'date'}))
                    elif field_type == 'time':
                        self.fields[key] = forms.TimeField(label=label, required=required,
                                              widget=forms.TimeInput(attrs={'type': 'time'}))
                    elif field_type == 'yesno':
                        self.fields[key] = forms.BooleanField(label=label, required=required)
                    else:
                        self.fields[key] = forms.CharField(label=label, required=required)
