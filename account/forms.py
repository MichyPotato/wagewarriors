from django import forms
from django.contrib.auth  import get_user_model

User = get_user_model()

class SeekerSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields[field].help_text = None

class RecruiterSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    company_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields[field].help_text = None


# Edit forms for profile updates
from .models import jobSeeker, recruiter


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
            # Leave checkbox styling to its specific widget
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
