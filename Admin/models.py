from enum import unique
from django.db import models

# Create your models here.

class Admin(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(unique=True,max_length=50)
    
class District(models.Model):
    district=models.CharField(max_length=50)
    
    def __str__(self):
        return self.district
    
class Place(models.Model):
    place=models.CharField(max_length=50)
    district=models.ForeignKey(District,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.place
    
class CrimeType(models.Model):
    crimetype=models.CharField(max_length=50)
    
    def __str__(self):
        return self.crimetype
    
    
    