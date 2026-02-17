from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from account.models import jobSeeker

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Applicants'
    template_data['applicants'] = jobSeeker.objects.all()
    return render(request, 'applicants/index.html', {'template_data': template_data})