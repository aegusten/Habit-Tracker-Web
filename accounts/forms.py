from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User, SecurityQuestion
from django.contrib.auth import authenticate

class RegisterForm(UserCreationForm):
    question1_subquestion = forms.ChoiceField(label="Select Question 1", required=True)
    answer1 = forms.CharField(label="Answer 1", required=True)

    question2_subquestion = forms.ChoiceField(label="Select Question 2", required=True)
    answer2 = forms.CharField(label="Answer 2", required=True)

    question3_subquestion = forms.ChoiceField(label="Select Question 3 (optional)", required=False)
    answer3 = forms.CharField(label="Answer 3 (optional)", required=False)

    class Meta:
        model = User
        fields = [ 'id_number', 'full_name', 'phone_number', 'age', 'password1', 'password2' ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        q1 = SecurityQuestion.objects.get(question_text="Security Question 1")
        q2 = SecurityQuestion.objects.get(question_text="Security Question 2")
        q3 = SecurityQuestion.objects.get(question_text="Security Question 3")

        self.fields['question1_subquestion'].choices = [
            (q1.option1, q1.option1),
            (q1.option2, q1.option2),
            (q1.option3, q1.option3),
        ]
        self.fields['question2_subquestion'].choices = [
            (q2.option1, q2.option1),
            (q2.option2, q2.option2),
            (q2.option3, q2.option3),
        ]
        self.fields['question3_subquestion'].choices = [
            (q3.option1, q3.option1),
            (q3.option2, q3.option2),
            (q3.option3, q3.option3),
        ]

    def clean(self):
        cleaned = super().clean()
        answers = [
            cleaned.get('answer1', '').strip(),
            cleaned.get('answer2', '').strip(),
            cleaned.get('answer3', '').strip()
        ]
        if sum(bool(a) for a in answers) < 2:
            raise forms.ValidationError("Please answer at least two security questions.")
        return cleaned


class LoginForm(forms.Form):
    id_number = forms.CharField(label='ID Number')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        id_number = self.cleaned_data.get('id_number')
        password = self.cleaned_data.get('password')

        if id_number and password:
            self.user_cache = authenticate(self.request, username=id_number, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid ID number or password.")
            if not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

class UpdatePersonalInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_number', 'age']
