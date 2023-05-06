from django.urls import path
from Agency import views
app_name='agency'

urlpatterns = [
    path('homeagency/',views.agencyhome,name="Agency-Home"),
    path('ag_profile/',views.ag_profile,name="Agency_Profile"),
    path('ag_editProf/<int:eagid>',views.ageditprof,name="AG_EditProfile"),
    path('ag_changepass/<int:cagid>',views.agchangepass,name="AG_ChangePwd"),
    path('crimevrf/',views.CrimeVrf,name="CrimeVerification"),
    path('acptcrime/',views.AcptCrime,name="AcceptedCrime"),
    path('rjctcrime/',views.RjctCrime,name="RejectedCrime"),
    path('agcmplnt/',views.AGCmplnt,name="AGComplaints"),  
    path('accpt_crime/<int:aid>',views.accept_crime,name="Accept_Crime"),
    path('rjct_crime/<int:rid>',views.reject_crime,name="Reject_Crime"),
    path('Key/<int:cid>', views.a_keyverification, name="Agency_Key"),
    path('Chat/', views.chat, name="Chat-agency"),
    path('loadchat/', views.loadchat, name="load-chat"),
]
