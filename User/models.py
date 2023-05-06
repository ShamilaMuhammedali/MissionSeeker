from django.db import models
from Guest.models import *

# Create your models here.

class Complaint(models.Model):
    content=models.TextField(null=True)
    reply=models.TextField(null=True)
    user=models.ForeignKey(NewUser,on_delete=models.SET_NULL,null=True)
    agency=models.ForeignKey(NewAgency,on_delete=models.SET_NULL,null=True)
    c_status=models.IntegerField(default=0)
    
    
class Crime(models.Model):
    crime_description=models.TextField(null=True)
    crimetype=models.ForeignKey(CrimeType,on_delete=models.CASCADE)
    user=models.ForeignKey(NewUser,on_delete=models.SET_NULL,null=True)
    agency=models.ForeignKey(NewAgency,on_delete=models.SET_NULL,null=True)
    c_vsts=models.IntegerField(default=0)
    
class Chat(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(
        NewUser, on_delete=models.SET_NULL, default=False, null=True, related_name="from_user")
    to_user = models.ForeignKey(
        NewUser, on_delete=models.SET_NULL, default=False, null=True, related_name="to_user")
    from_agency = models.ForeignKey(
        NewAgency, on_delete=models.SET_NULL, default=False, null=True, related_name="from_agency")
    to_agency = models.ForeignKey(
        NewAgency, on_delete=models.SET_NULL, default=False, null=True, related_name="to_agency")
    content = models.BinaryField(max_length=10000)
    