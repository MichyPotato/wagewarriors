from django.shortcuts import render

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Account'
    return render(request, 'account/index.html', {'template_data': template_data})