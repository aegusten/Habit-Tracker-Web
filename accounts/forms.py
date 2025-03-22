from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    pet_name = forms.CharField(required=True, label="What is your pet's name?")
    first_love = forms.CharField(required=True, label="Who was your first love?")
    favorite_color = forms.CharField(required=False, label="What is your favorite color?")

    class Meta:
        model = User
        fields = [
            'id_number', 'full_name', 'phone_number', 'age',
            'pet_name', 'first_love', 'favorite_color',
            'password1', 'password2'
        ]
        labels = {'id_number': 'ID Number'}

    def clean(self):
        cleaned = super().clean()
        answers = [
            bool(cleaned.get('pet_name')),
            bool(cleaned.get('first_love')),
            bool(cleaned.get('favorite_color')),
        ]
        if sum(answers) < 2:
            raise forms.ValidationError("Please answer at least two security questions.")
        return cleaned

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='ID Number')

class UpdatePersonalInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_number', 'age']
