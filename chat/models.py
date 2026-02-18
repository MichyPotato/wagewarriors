from django.db import models

# Create your models here.
class messages(models.Model):
    recruiterIDFK = models.ForeignKey('account.recruiter', on_delete=models.CASCADE)
    jobSeekerIDFK = models.ForeignKey('account.jobSeeker', on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recruiterIDFK.user.username}-{self.jobSeekerIDFK.user.username}-{self.timestamp}"