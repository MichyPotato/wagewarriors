from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from .models import jobSeeker, recruiter
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe

User = get_user_model()

class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))

class SeekerSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field.startswith('password'):
                self.fields[field].widget.attrs.update({'class': 'form-control'})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields[field].help_text = None


class RecruiterSignupForm(UserCreationForm):
    company_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'company_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields[field].help_text = None

# Edit forms for profile updates
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = jobSeeker
        fields = ['currentLocation', 'headline', 'skills', 'education', 'work_experience', 'additional_links', 'isPrivate']
        widgets = {
            'isPrivate': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'isPrivate':
                continue
            widget = self.fields[field].widget
            try:
                widget.attrs.update({'class': 'form-control'})
            except Exception:
                pass

class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = recruiter
        fields = ['company_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
