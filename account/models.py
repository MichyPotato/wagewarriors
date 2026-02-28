from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_job_seeker = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=False)

class jobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='job_seeker_profile')
    currentLocation = models.CharField(max_length=100, blank=True)
    headline = models.CharField(max_length=255, blank=True)
    skills = models.TextField(blank=True)
    education = models.TextField(blank=True)
    work_experience = models.TextField(blank=True)
    additional_links = models.TextField(blank=True)
    isPrivate = models.BooleanField(default=False)
    # curLat = models.FloatField(default=0.0, blank=True)
    # curLong = models.FloatField(default=0.0, blank=True)

    def __str__(self):
        return self.user.username

class recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile')
    company_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username

class jobsAppliedTo(models.Model):
    jobIDFK = models.ForeignKey('jobs.job', on_delete=models.CASCADE)
    jobSeekerIDFK = models.ForeignKey(jobSeeker, on_delete=models.CASCADE)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('Applied', 'Applied'),
        ('Review', 'Review'),
        ('Interview', 'Interview'),
        ('Offer', 'Offer'),
        ('Closed', 'Closed'),
        ('Rejected', 'Rejected')
    ], default='Applied')

    def __str__(self):
        return f"{self.jobSeekerIDFK.user.username} - {self.jobIDFK.title}"