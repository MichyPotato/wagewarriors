from django.db import models

# Create your models here.
class Location(models.Model):
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.city}, {self.state}, {self.country} ({self.latitude}, {self.longitude})"