from django.shortcuts import render
from .forms import seekerForm, recruiterForm
from django.shortcuts import redirect

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Account'
    return render(request, 'account/index.html', {'template_data': template_data})

def login(request):
    return render(request, 'account/login.html')

def seeker_signup(request):
    form = seekerForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('account.login') #change to a redirect to the login page
    return render(request, 'account/seeker_signup.html', {'form': form})
    
def recruiter_signup(request):
    form = recruiterForm(request.POST)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('account.login') #change to a redirect to the login page
    return render(request, 'account/recruiter_signup.html', {'form': form})