from enum import unique
from django.db import models
from Admin.models import *

# Create your models here.

class NewUser(models.Model):
    name=models.CharField(max_length=50)
    contact=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    address=models.TextField(null=True)
    gender=models.CharField(max_length=50)
    place=models.ForeignKey(Place,on_delete=models.CASCADE)
    password=models.CharField(unique=True,max_length=50)
    key=models.BinaryField(max_length=1000,null=True)
    
class NewAgency(models.Model):
    ag_name=models.CharField(max_length=50)
    ag_email=models.EmailField(unique=True)
    ag_logo=models.FileField(upload_to='agencydocs/')
    ag_proof=models.FileField(upload_to='agencydocs/')
    ag_password=models.CharField(unique=True,max_length=50)
    crimetype=models.ForeignKey(CrimeType,on_delete=models.CASCADE)
    ag_status=models.IntegerField(default=False)
    keys=models.BinaryField(max_length=1000,null=True)
   
    