from django.db import models
from datetime import date


class LocationData(models.Model):
    city = models.CharField(max_length=30)
    location= models.CharField(max_length=90)
    latitude = models.DecimalField(max_digits=16, decimal_places=14)
    longtitude = models.DecimalField(max_digits=17, decimal_places=14)
    def __str__(self):
        return f'{self.city}, {self.location}'

class Offer(models.Model):
    # dodać link, picture, 
    location_data = models.ForeignKey(LocationData, on_delete=models.CASCADE, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pricesqm = models.DecimalField(max_digits=7, decimal_places=2)
    size = models.DecimalField(max_digits=6, decimal_places=2)
    link = models.CharField(max_length=255)
    picture = models.CharField(max_length=255)
    date_of_scraping = models.DateField(default=date.today)
    def __str__(self):
        return f'{self.location_data}, {self.date_of_scraping}'


