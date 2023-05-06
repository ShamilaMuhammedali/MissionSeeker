from django.urls import path
from User import views
app_name='user'

urlpatterns = [
    path('homeuser/',views.userhome,name="User-Home"),
    path('userprofile/',views.uprofile,name="User_Profile"),
    path('editprof/<int:euid>',views.ueditprof,name="U_EditProfile"),
    path('changepass/<int:cuid>',views.uchangepass,name="U_ChangePwd"),
    path('ucomplaint/',views.UComplaint,name="UComplaint"),
    path('search_agency/',views.SearchAg,name="SearchAgency"),
    path('get_agency/',views.getAgency,name="GetAgency"),
    path('crime/<int:aid>',views.crime,name="Crime"),
    path('Key/<int:cid>', views.keyverification, name="User_Key"),
    path('Chat/', views.chatuser, name="Chat-user"),
    path('loadchat/', views.loadchatuser, name="load-chat"),
]