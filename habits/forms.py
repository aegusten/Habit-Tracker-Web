from django import forms
from .models import Habit

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name','timeline','motivational_reminder','insights_method']

class HabitRecordForm(forms.Form):
    def __init__(self, *args, metrics=None, **kwargs):
        super().__init__(*args, **kwargs)
        for key in metrics.keys():
            self.fields[key] = forms.FloatField(required=False, label=key.replace('_',' ').title())
