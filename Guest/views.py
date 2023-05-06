from django.shortcuts import render,redirect
from cryptography.fernet import Fernet
from Guest.models import *
from Admin.models import *
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

def home(request):
    return render(request,"Guest/Home.html")

def newuser(request):
    dist=District.objects.all()
    if request.method=="POST":
        genwrite_key()
        plcid=request.POST.get('sel_plc')
        plc=Place.objects.get(id=plcid)
        name=request.POST.get('txt_name')
        email1=request.POST.get('txt_email')
        key = call_key()
        str1=key.decode()
        send_mail(
            'Respected sir/madam '+name, #subject
            "\r Your Encryption Key is "+str1+"Thank you.",#body
            settings.EMAIL_HOST_USER,
            [email1],

        )
        NewUser.objects.create(name=request.POST.get('txt_name'),contact=request.POST.get('txt_cntct'),
        email=request.POST.get('txt_email'),address=request.POST.get('txt_address'),gender=request.POST.get('gender'),
        place=plc,password=request.POST.get('txt_pwd'),key=key)
        return render(request,"Guest/NewUser.html",{'Dis':dist})
    else:
        return render(request,"Guest/NewUser.html",{'Dis':dist})
    
def ajaxplace(request):
    dist=request.GET.get('district')
    plc=Place.objects.filter(district=dist)
    return render(request,"Guest/AjaxPlace.html",{'PLC':plc})

def login(request):
    if request.method=="POST":
        
        Email=request.POST.get('txt_email')
        Password=request.POST.get('txt_pass')
        adminlog=Admin.objects.filter(email=Email,password=Password).count()
        userlog=NewUser.objects.filter(email=Email,password=Password).count()
        agencylog=NewAgency.objects.filter(ag_email=Email,ag_password=Password,ag_status=True).count()
        if adminlog > 0:
            admin=Admin.objects.get(email=Email,password=Password)
            request.session['aid']=admin.id
            return redirect('webadmin:Admin-Home')
        elif userlog > 0:
            user=NewUser.objects.get(email=Email,password=Password)
            request.session['uid']=user.id
            return redirect('user:User-Home')
        elif agencylog > 0:
            agency=NewAgency.objects.get(ag_email=Email,ag_password=Password,ag_status=1)
            request.session['agid']=agency.id
            return redirect('agency:Agency-Home')
        else:
            error="Invalid Details"
            return render(request,"Guest/Login.html",{"Error":error})
    else:
        return render(request,"Guest/Login.html")
    
def newagency(request):
    ctype=CrimeType.objects.all()
    if request.method=="POST" and request.FILES:
        genwrite_key()
        ctid=request.POST.get('sel_crimetype')
        ct=CrimeType.objects.get(id=ctid)
        name=request.POST.get('txt_name')
        email1=request.POST.get('txt_email')
        key = call_key()
        str1=key.decode()
        send_mail(
            'Respected sir/madam '+name, #subject
            "\r Your Encryption Key is "+str1+"Thank you.",#body
            settings.EMAIL_HOST_USER,
            [email1],

        )
        NewAgency.objects.create(ag_name=request.POST.get('txt_name'),ag_email=request.POST.get('txt_email'),
        ag_logo=request.FILES.get('logo'),ag_proof=request.FILES.get('proof'),ag_password=request.POST.get('txt_pass'),
        crimetype=ct,keys=key)  
        return render(request,"Guest/NewAgency.html",{'CT':ctype}) 
    else: 
        return render(request,"Guest/NewAgency.html",{'CT':ctype})
    



def genwrite_key():
    key = Fernet.generate_key()
    with open("pass.key", "wb") as key_file:
        key_file.write(key)

def call_key():
    return open("pass.key", "rb").read()