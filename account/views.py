from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SeekerSignupForm, RecruiterSignupForm, CustomErrorList
from .models import jobSeeker, recruiter, User, jobsAppliedTo
from .forms import UserEditForm, JobSeekerProfileForm, RecruiterProfileForm
from django.contrib.auth import logout
from jobs.models import job
from django.http import JsonResponse, HttpResponseBadRequest, Http404
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied 


# Create your views here.
#Landing page to let users sign up as a job seeker or recruiter
def index(request):
    template_data = {}
    template_data['title'] = 'Account'
    return render(request, 'account/index.html', {'template_data': template_data})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            if user.is_job_seeker:
                return redirect('account.profile', username=user.username)
            elif user.is_recruiter:
                return redirect('account.profile', username=user.username)
            else:
                return redirect('home.index')
        else:
            pass
    else:
        form = AuthenticationForm()
    
    return render(request, 'account/login.html', {'form': form})


# Loads user's profile
@login_required
def profile(request, username):
    template_data = {}
    template_data['title'] = 'Profile'
    user = get_object_or_404(User, username=username)
    return render(request, 'account/profile.html', {'template_data': template_data, 'user': user})

# Edits user's profile
@login_required
def edit_profile(request, username):
    if request.user.username != username:
        return redirect('account.profile', username=username)

    user_obj = request.user

    # Ensure profile instances exist
    if user_obj.is_job_seeker:
        try:
            profile_instance = user_obj.job_seeker_profile
        except jobSeeker.DoesNotExist:
            profile_instance = jobSeeker.objects.create(user=user_obj)
    elif user_obj.is_recruiter:
        try:
            profile_instance = user_obj.recruiter_profile
        except recruiter.DoesNotExist:
            profile_instance = recruiter.objects.create(user=user_obj)
    else:
        profile_instance = None

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user_obj)

        if user_obj.is_job_seeker:
            profile_form = JobSeekerProfileForm(request.POST, error_class=CustomErrorList, instance=profile_instance)
        elif user_obj.is_recruiter:
            profile_form = RecruiterProfileForm(request.POST, error_class=CustomErrorList, instance=profile_instance)
        else:
            profile_form = None

        forms_valid = user_form.is_valid() and (profile_form.is_valid() if profile_form else True)

        if forms_valid:
            user_form.save()
            if profile_form:
                profile_form.save()
            return redirect('account.profile', username=user_obj.username)
    else:
        user_form = UserEditForm(instance=user_obj)
        if user_obj.is_job_seeker:
            profile_form = JobSeekerProfileForm(instance=profile_instance)
        elif user_obj.is_recruiter:
            profile_form = RecruiterProfileForm(instance=profile_instance)
        else:
            profile_form = None

    return render(request, 'account/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_obj': user_obj,
        'template_data': {'title': 'Edit Profile'},
    })

#logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('home.index')

def seeker_signup(request):
    if request.method == 'POST':
        form = SeekerSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_job_seeker = True
            user.save()
            jobSeeker.objects.create(user=user)
            return redirect('account.login')
    else:
        form = SeekerSignupForm()
    return render(request, 'account/seeker_signup.html', {'form': form})
    
def recruiter_signup(request):
    if request.method == 'POST':
        form = RecruiterSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_recruiter = True
            user.save()
            recruiter_profile = recruiter.objects.create(user=user)
            recruiter_profile.company_name = form.cleaned_data.get('company_name', '')
            recruiter_profile.save()
            return redirect('account.login')
    else:
        form = RecruiterSignupForm()
    return render(request, 'account/recruiter_signup.html', {'form': form})

def applications(request, username):
    user = get_object_or_404(User, username=username)
    if not user.is_job_seeker:
        return redirect('account.profile', username=username)

    job_seeker_profile = get_object_or_404(jobSeeker, user=user)
    applications = jobSeeker.objects.filter(user=user).first().jobsappliedto_set.select_related('jobIDFK')

    template_data = {
        'title': 'My Applications',
        'applications': applications,
    }
    return render(request, 'account/applications.html', {'template_data': template_data, 'user': user})

def recruiter_job(request):
    if not request.user.is_authenticated or not getattr(request.user, 'is_recruiter', False):
        return job.objects.none()
    company = getattr(request.user.recruiter_profile, 'company_name', '') or ''
    return job.objects.filter(company=company)

@login_required
def kanban(request, job_id=None):
    if not getattr(request.user, 'is_recruiter', False):
        return redirect('jobs.index')
    recruiter_jobs = recruiter_job(request)
    if job_id is not None:
        job_instance = get_object_or_404(job, id=job_id)
        if job_instance not in recruiter_job
            return redirect('account.kanban')
        applications = jobsAppliedTo.objects.filter(JobIDFK=job_instance).select_related('jobSeekerIDFK', 'jobSeekerIDFK__user').order_by('status', 'jobSeekerIDFK__user__username')
        status = [c[0] for c in jobsAppliedTo._meta.get_field('status').choices]
    
        template_data = {}
        template_data['title'] = f'Pipeline: {job_instance.title}'
        template_data['job'] = job_instance
        template_data['applications'] = applications
        template_data['status'] = status

        return render(request, 'account/kanban.html', {'template_data': template_data})
    template_data = {}
    template_data['title'] = 'Applicant Pipeline'
    template_data['jobs'] = recruiter_job

    return render(request, 'account/kanban_job.html' {'template_data': template_data})
