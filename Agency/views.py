from django.shortcuts import render,redirect
from cryptography.fernet import Fernet
from Guest.models import NewAgency
from User.models import *

# Create your views here.

def agencyhome(request):
    
    return render(request,"Agency/Agency_Home.html")

def ag_profile(request):
    profile=NewAgency.objects.get(id=request.session['agid'])
    return render(request,"Agency/AG_Profile.html",{'AP':profile})

def ageditprof(request,eagid):
    if "agid" in request.session:
        selAG=NewAgency.objects.get(id=eagid)
        if request.method=="POST":
            selAG.ag_name=request.POST.get('txtname')
            selAG.ag_email=request.POST.get('txtemail')
            selAG.save()
            return redirect('agency:Agency_Profile')
        else:
            return render(request,"Agency/AG_EditProfile.html",{'EP':selAG})
    else:
        return redirect('guest:Login')
    
def agchangepass(request,cagid):
    change=NewAgency.objects.get(id=cagid)
    pwd=change.ag_password
    if request.method=="POST":
        old=request.POST.get('cpwd')
        if old!=pwd:
            error="Password Not Correct"
            return render(request,"Agency/AG_ChangePassword.html",{'Error':error})
        else:
            new=request.POST.get('npwd')
            change=NewAgency.objects.get(id=cagid)
            change.ag_password=new
            change.save()
            return redirect('guest:Login')
    else:
        return render(request,"Agency/AG_ChangePassword.html")

def CrimeVrf(request):
    cv=Crime.objects.filter(agency=request.session['agid'])
    return render(request,"Agency/Crime_verification.html",{'C':cv})


def a_keyverification(request,cid):
    request.session['aid']=cid
    
    agnid=NewAgency.objects.get(id=request.session['agid'])
    K=agnid.keys
    print(K)
        
    if request.method=="POST":
        Key=request.POST.get('en_key')
        Key = Key.encode()
        if Key==K:
            return redirect('agency:Chat-agency')
        else:
            error="Key Incorrect!!"
            return render(request,"Agency/KeyVerification.html",{'ERROR':error})
    else:
        return render(request,"Agency/KeyVerification.html")
    

def accept_crime(request,aid):
    ac=Crime.objects.get(id=aid)
    ac.c_vsts=1
    ac.save()
    return redirect('agency:CrimeVerification')


def reject_crime(request,rid):
    rc=Crime.objects.get(id=rid)
    rc.c_vsts=2
    rc.save()
    return redirect('agency:CrimeVerification')

def AcptCrime(request):
    cv=Crime.objects.filter(c_vsts=1,agency=request.session['agid'])
    return render(request,"Agency/Accepted_Crime.html",{'C':cv})

def RjctCrime(request):
    cv=Crime.objects.filter(c_vsts=2,agency=request.session['agid'])
    return render(request,"Agency/Rejected_crime.html",{'C':cv})

def AGCmplnt(request):
    if request.method=="POST":
        Agency=NewAgency.objects.get(id=request.session['agid'])
        Complaint.objects.create(content=request.POST.get('txtcontent'),agency=Agency)
        cmp=Complaint.objects.filter(agency=request.session['agid'])
        return render(request,"Agency/AG_Complaint.html",{'CMP':cmp})
    else:
        cmp=Complaint.objects.filter(user=request.session['agid'])
        return render(request,"Agency/AG_Complaint.html",{'CMP':cmp})
    
    
def chat(request):
    chatobj = Crime.objects.get(id=request.session["aid"])
    if request.method == "POST":
        cied = request.POST.get("cid")
        # print(cied)
        ciedobj = NewUser.objects.get(id=cied)
        key=ciedobj.key
        a=Fernet(key)
        sobj = NewAgency.objects.get(id=request.session["agid"])
        content = request.POST.get("msg")
        slog=content.encode()
        encrypted=a.encrypt(slog)
        # print(cied)
        print(content)
        Chat.objects.create(
            from_agency=sobj, to_user=ciedobj, content=encrypted, from_user=None, to_agency=None)
        return render(request, 'Agency/Chat.html', {"chatobj": chatobj})
    else:
        return render(request, 'Agency/Chat.html', {"chatobj": chatobj})


def loadchat(request):
    cid = request.GET.get("cid")
    request.session["cid"] = cid

    cid1 = request.session["cid"]
    # print(cid1)

    # print(cid)
    shopobj = NewUser.objects.get(id=cid)
    key1=shopobj.key
    
    b=Fernet(key1)
    
    # print(userobj)
    sid = request.session["agid"]
    
    # print(sid)
    suserobj = NewAgency.objects.get(id=request.session["agid"])
    key=suserobj.keys
    a=Fernet(key)

    chatobj = Chat.objects.raw(
        "select * from User_chat c inner join Guest_newagency u on (u.id=c.from_agency_id) or (u.id=c.to_agency_id) WHERE  c.from_user_id=%s or c.to_user_id=%s order by c.date", params=[(cid1), (cid1)])
    
    leh=(len(chatobj))
    message=[0 for i in range(0,leh)]
    
    for i in range(0,leh):
        csid=int(cid)
        if chatobj[i].from_user_id==csid and chatobj[i].to_agency_id==sid:
            chatobj[i].content=a.decrypt(chatobj[i].content).decode()
        elif chatobj[i].to_user_id==csid and chatobj[i].from_agency_id==sid:
            chatobj[i].content=b.decrypt(chatobj[i].content).decode()
    # print(message)   
    lk=[0 for i in range(0,leh)]  
    for i in range(0,leh):
        lk[i]=i
    return render(request, 'Agency/Load.html', {"obj": chatobj, "sid": sid, "shop": shopobj, "userobj": suserobj,'content':message,'len':lk})
