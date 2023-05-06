from django.shortcuts import render,redirect

from Admin.models import *
from Guest.models import *
from User.models import *

# Create your views here.

def AdminHome(request):
    admin=Admin.objects.get(id=request.session['aid'])
    return render(request,"Admin/Admin_Home.html",{'A':admin})

def dis(request):
    if request.method=="POST":
        District.objects.create(district=request.POST.get('txt_dis'))
        dis=District.objects.all()
        return render(request,"Admin/District.html",{'Dis':dis})
    else:
        dis=District.objects.all()
        return render(request,"Admin/District.html",{'Dis':dis})
    
def dltdis(request,did):
    District.objects.get(id=did).delete()
    return redirect('webadmin:District')

def updis(request,uid):
    seldis=District.objects.get(id=uid)
    if request.method=="POST":
        seldis.district=request.POST.get('txt_dis')
        seldis.save()
        return redirect('webadmin:District')
    else:
        return render(request,"Admin/EditDis.html",{'SD':seldis})
    
def plc(request):
    disob=District.objects.all()
    if request.method=="POST":
        disid=request.POST.get('sel_dis')
        dis=District.objects.get(id=disid)
        Place.objects.create(place=request.POST.get('txt_plc'),district=dis)
        plcob=Place.objects.all()
        return render(request,"Admin/Place.html",{'DS':disob,'Plc':plcob})
    else:
        plcob=Place.objects.all()
        return render(request,"Admin/Place.html",{'DS':disob,'Plc':plcob})
    
def dltplc(request,dpid):
    Place.objects.get(id=dpid).delete()
    return redirect('webadmin:Place')

def upplc(request,upid):
    disob=District.objects.all()
    selplc=Place.objects.get(id=upid)
    if request.method=="POST":
        dist=request.POST.get('sel_dis')
        selplc.district=District.objects.get(id=dist)
        selplc.place=request.POST.get('txt_plc')
        selplc.save()
        return redirect('webadmin:Place')
    else:
        return render(request,"Admin/EditPlc.html",{'SP':selplc,'DS':disob})

def ct(request):
    if request.method=="POST":
        CrimeType.objects.create(crimetype=request.POST.get('txt_ct'))
        ctype=CrimeType.objects.all()
        return render(request,"Admin/CrimeType.html",{'CT':ctype})
    else:
        ctype=CrimeType.objects.all()
        return render(request,"Admin/CrimeType.html",{'CT':ctype})
    
def dltct(request,dctid):
    CrimeType.objects.get(id=dctid).delete()
    return redirect('webadmin:CrimeType')

def upct(request,uctid):
    selct=CrimeType.objects.get(id=uctid)
    if request.method=="POST":
        selct.crimetype=request.POST.get('txt_ct')
        selct.save()
        return redirect('webadmin:CrimeType')
    else:
        return render(request,"Admin/EditCrimeType.html",{'CT':selct})

def AgVrf(request):
    ag=NewAgency.objects.filter(ag_status=0)
    return render(request,"Admin/Agency_Verification.html",{'AV':ag})

def accptag(request,aid):
    accpt=NewAgency.objects.get(id=aid)
    accpt.ag_status=True 
    accpt.save()
    return redirect('webadmin:AgencyVerification')

def rjctag(request,rid):
    rjct=NewAgency.objects.get(id=rid)
    rjct.ag_status=2
    rjct.save()
    return redirect('webadmin:AgencyVerification')

def AcptAg(request):
    aa=NewAgency.objects.filter(ag_status=1)
    return render(request,"Admin/Accepted_Agencies.html",{'AA':aa})

def RjctAg(request):
    ra=NewAgency.objects.filter(ag_status=2)
    return render(request,"Admin/Rejected_Agencies.html",{'RA':ra})

def NwUsrLst(request):
    ul=NewUser.objects.all()
    return render(request,"Admin/New_User_List.html",{'UL':ul})

def Cmplnt(request):
    usr=Complaint.objects.filter(user_id__gt=0)
    ag=Complaint.objects.filter(agency_id__gt=0)
    return render(request,"Admin/Complaints.html",{'U':usr,'A':ag})

def Reply(request,rid):
    cmp=Complaint.objects.get(id=rid)
    if request.method=="POST":
        cmp.reply=request.POST.get('txtreply')
        cmp.c_status=1
        cmp.save()
        return redirect('webadmin:Complaints')
    else:
        return render(request,"Admin/Reply.html",{'RP':cmp})