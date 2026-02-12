from django import forms
from .models import jobSeeker, recruiter

class seekerForm(forms.ModelForm):
    class Meta:
        model = jobSeeker
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['name', 'email', 'username', 'password', 
                          'currentLocation', 'headline','skills', 'education',
                          'work_experience', 'additional_links']:
            self.fields[fieldname].widget.attrs.update( {'class': 'form-control'})
        
class recruiterForm(forms.ModelForm):
    class Meta:
        model = recruiter
        fields = ['name', 'email', 'username', 'password', 'company_name']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['name', 'email', 'username', 'password', 'company_name']:
            self.fields[fieldname].widget.attrs.update( {'class': 'form-control'})