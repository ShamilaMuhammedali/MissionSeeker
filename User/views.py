from django.shortcuts import redirect, render
from cryptography.fernet import Fernet
from Guest.models import *
from User.models import *

# Create your views here.

def userhome(request):
    user=NewUser.objects.get(id=request.session['uid'])
    return render(request,"User/User_Home.html",{'U':user})

def uprofile(request):
    profile=NewUser.objects.get(id=request.session['uid'])
    return render(request,"User/U_Profile.html",{'Profile':profile})

def ueditprof(request,euid):
    if "uid" in request.session:
        selU=NewUser.objects.get(id=euid)
        if request.method=="POST":
            selU.name=request.POST.get('txtname')
            selU.contact=request.POST.get('txtcntct')
            selU.email=request.POST.get('txtemail')
            selU.address=request.POST.get('txtaddress')
            selU.save()
            return redirect('user:User_Profile')
        else:
            return render(request,"User/U_EditProfile.html",{'EP':selU})
    else:
        return redirect('guest:Login')
    
def uchangepass(request,cuid):
    change=NewUser.objects.get(id=cuid)
    pwd=change.password
    if request.method=="POST":
        old=request.POST.get('cpwd')
        if old!=pwd:
            error="Password Not Correct"
            return render(request,"User/U_ChangePassword.html",{'Error':error})
        else:
            new=request.POST.get('npwd')
            change=NewUser.objects.get(id=cuid)
            change.password=new
            change.save()
            return redirect('guest:Login')
    else:
        return render(request,"User/U_ChangePassword.html")

def UComplaint(request):
    if request.method=="POST":
        User=NewUser.objects.get(id=request.session['uid'])
        Complaint.objects.create(content=request.POST.get('txtcontent'),user=User)
        cmp=Complaint.objects.filter(user=request.session['uid'])
        return render(request,"User/U_Complaint.html",{'CMP':cmp})
    else:
        cmp=Complaint.objects.filter(user=request.session['uid'])
        return render(request,"User/U_Complaint.html",{'CMP':cmp})


def SearchAg(request):
    dist=District.objects.all()
    ctype=CrimeType.objects.all()
    ag=NewAgency.objects.all()
    return render(request,"User/Search_Agency.html",{'Dis':dist,'CT':ctype,'Ag':ag})

def getAgency(request):
    ctype=request.GET.get('crimetype')
    ag=NewAgency.objects.filter(crimetype=ctype)
    return render(request,"User/GetAgency.html",{'AG':ag})
 
 
def crime(request,aid):
    agencyid=NewAgency.objects.get(id=aid)
    ctype=CrimeType.objects.all()
    if request.method=="POST":
        userid=NewUser.objects.get(id=request.session['uid'])         
        ctid=request.POST.get('sel_crimetype')
        ct=CrimeType.objects.get(id=ctid)
        Crime.objects.create(crime_description=request.POST.get('txtdes'),crimetype=ct,agency=agencyid,user=userid)
        cm=Crime.objects.filter(user=request.session['uid'],agency=agencyid)
        return render(request,"User/Crime.html",{'CT':ctype,'CM':cm})
    else:
        cm=Crime.objects.filter(user=request.session['uid'],agency=agencyid)
        return render(request,"User/Crime.html",{'CT':ctype,'CM':cm})
    
def keyverification(request,cid):
    request.session['did']=cid
    
    userid=NewUser.objects.get(id=request.session['uid'])
    K=userid.key
    print(K)
        
    if request.method=="POST":
        Key=request.POST.get('en_key')
        Key = Key.encode()
        if Key==K:
            return redirect('user:Chat-user')
        else:
            error="Key Incorrect!!"
            return render(request,"User/KeyVerification.html",{'ERROR':error})
    else:
        return render(request,"User/KeyVerification.html")
        
    
def chatuser(request):
    chatobj = Crime.objects.get(id=request.session["did"])
    if request.method == "POST":
       
        cied = request.POST.get("cid")
        # print(cied)
        ciedobj = NewAgency.objects.get(id=cied)
        key=ciedobj.keys
        a=Fernet(key)

        '''key=bytes(key,'utf-8')
        print(key)
        with open("pass.key", "wb") as key_file:
            key_file.write(key)
        key=call_key()
        
        key=key.decode('utf-8')
        key=base64.urlsafe_b64encode(bytes(key,'utf-8'))
        print(key)
        a=Fernet(key)'''
        sobj = NewUser.objects.get(id=request.session["uid"])
        content = request.POST.get("msg")
        slog=content.encode()
        coded_slog=a.encrypt(slog)
        print("Encrypted")
        print(coded_slog)
        decoded_slog=a.decrypt(coded_slog)
        print("Decrypted")
        
        cont=decoded_slog.decode()
        print(cont)
        # print(cied)
        # print(content)
        Chat.objects.create(
            from_user=sobj, to_agency=ciedobj, content=coded_slog, from_agency=None, to_user=None)
        return render(request, 'User/Chat.html', {"chatobj": chatobj})
    else:
        return render(request, 'User/Chat.html', {"chatobj": chatobj})


def loadchatuser(request):
    cid = request.GET.get("cid")
    request.session["cid"] = cid

    cid1 = request.session["cid"]
    # print(cid1)

    # print(cid)
    shopobj = NewAgency.objects.get(id=cid)
    key=shopobj.keys
    a=Fernet(key)
    # print(userobj)
    sid = request.session["uid"]
    # print(sid)
    suserobj = NewUser.objects.get(id=request.session["uid"])
    key1=suserobj.key
    b=Fernet(key1)
    # chatobj1 = Chat.objects.filter(Q(to_user=suserobj) | Q(
    #     from_user=suserobj), Q(to_shop=shopobj) | Q(from_shop=shopobj))
    # print(chatobj1)  # send message

    # print(chatobj2)  # recived msg
    chatobj = Chat.objects.raw(
        "select * from User_chat c inner join Guest_newuser u on (u.id=c.from_user_id) or (u.id=c.to_user_id) WHERE  c.from_agency_id=%s or c.to_agency_id=%s order by c.date", params=[(cid1), (cid1)])
    

    leh=(len(chatobj))
    #message=[0 for i in range(0,leh)]
    for i in range(0,leh):
        csid=int(cid)
        if chatobj[i].from_user_id==sid and chatobj[i].to_agency_id==csid:
            chatobj[i].content=a.decrypt(chatobj[i].content).decode()
        elif chatobj[i].to_user_id==sid and chatobj[i].from_agency_id==csid:
            chatobj[i].content=b.decrypt(chatobj[i].content).decode()
    #print(message)
        

    return render(request, 'User/Load.html', {"obj":chatobj, "sid": sid, "shop": shopobj, "userobj": suserobj})

     

def call_key():
    return open("pass.key", "rb").read()