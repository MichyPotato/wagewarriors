from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from .models import job
from decimal import Decimal, InvalidOperation

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Jobs'
    jobList = job.objects.all()

    title = request.GET.get('title')
    location = request.GET.get('location')
    skill = request.GET.get('skill')
    min = request.GET.get('min_salary')
    max = request.GET.get('max_salary')
    remote = request.GET.get('isRemote')
    visa = request.GET.get('hasVisaSponsorship')

    if title:
        jobList = jobList.filter(title__icontains=title)
    if location:
        jobList = jobList.filter(location__icontains=location)
    if skill:
        jobList = jobList.filter(skills__icontains=skill)
    if min:
        jobList = jobList.filter(salaryLower__gte=min)
    if max:
        jobList = jobList.filter(salaryUpper__lte=max)
    if remote == 'on':
        jobList = jobList.filter(isRemote=True)
    if visa == 'on':
        jobList = jobList.filter(hasVisaSponsorship=True)
    
    template_data['jobs'] = jobList
    return render(request, 'jobs/index.html', {'template_data': template_data})

def apply(request, id):
    job_instance = get_object_or_404(job, id=id)

    context = {
        'job': job_instance,
    }

    return render(request, 'jobs/applied.html', context)


def create_or_edit(request, id=None):
    if not request.user.is_recruiter:
        return redirect('jobs.index')
    
    if id:
        job_instance = get_object_or_404(job, id=id)
        if job_instance.company != request.user.recruiter_profile.company_name:
            return redirect('jobs.index')
    else:
        job_instance = job()

    if request.method == "POST":
        try:
            job_instance.salaryLower = Decimal(request.POST.get('salaryLower')).quantize(Decimal('0.00'))
            job_instance.salaryUpper = Decimal(request.POST.get('salaryUpper')).quantize(Decimal('0.00'))

            if job_instance.salaryLower > job_instance.salaryUpper:
                messages.error(request, "Lower salary cannot be higher than upper salary.")
                return render(request, 'jobs/edit.html', {'job': job_instance, 'new_job': False})
        except (InvalidOperation, TypeError):
            messages.error(request, "Please enter a valid decimal number for salary.")
            return render(request, 'jobs/edit.html', {'job': job_instance, 'new_job': False})
        
        if not id:
            job_instance.company = request.user.recruiter_profile.company_name

        job_instance.title = request.POST.get('title')
        job_instance.location = request.POST.get('location')
        if request.POST.get('isRemote'):
            job_instance.isRemote = True
        else:
            job_instance.isRemote = False
        if request.POST.get('hasVisaSponsorship'):
            job_instance.hasVisaSponsorship = True
        else:
            job_instance.hasVisaSponsorship = False
        job_instance.description = request.POST.get('description')

        skills_raw = request.POST.get('skills', '')
        job_instance.skills = [s.strip() for s in skills_raw.split(',') if s.strip()]
        
        job_instance.save()

        messages.success(request, "Job posting edited successfully.")
        return redirect('jobs.index')

    mode = {
        'job': job_instance,
        'editing': bool(id), 
    }
    return render(request, 'jobs/edit.html', mode)