# points/models.py
from django.db import models

class Point(models.Model):
    geolocation = models.CharField(max_length=100)  # e.g., "lat,lng"
    date = models.DateField()
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    length = models.FloatField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)
    fire_status = models.CharField(max_length=10, choices=[
        ('biomass', 'Biomass'),
        ('active', 'Active Burning'),
        ('burnt', 'Already Burnt'),
    ])
    image = models.ImageField(upload_to='point_images/', blank=True, null=True)

    def __str__(self):
        return f'{self.city}, {self.state} - {self.fire_status}'
