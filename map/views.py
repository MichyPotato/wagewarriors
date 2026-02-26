from django.shortcuts import render
from .models import Location

# Create your views here.
def index(request):
  cities = list(Location.objects.values('city', 'state', 'country', 'latitude', 'longitude')[19700:20000])  # Get the first 100 locations
  context = {'cities': cities}
  return render(request, 'map/index.html', context)

