from django.urls import path
from Admin import views
app_name='webadmin'

urlpatterns = [
    path('homeA/',views.AdminHome,name="Admin-Home"),
    path('dis/',views.dis,name="District"),
    path('dltdis/<int:did>',views.dltdis,name="Dlt_Dis"),
    path('updis/<int:uid>',views.updis,name="Up_Dis"),
    path('plc/',views.plc,name="Place"),
    path('dltplc/<int:dpid>',views.dltplc,name="Dlt_Plc"),
    path('upplc/<int:upid>',views.upplc,name="Up_Plc"),
    path('crimetype/',views.ct,name="CrimeType"),
    path('dltct/<int:dctid>',views.dltct,name="Dlt_CT"),
    path('upct/<int:uctid>',views.upct,name="Up_CT"),
    path('agvrf/',views.AgVrf,name="AgencyVerification"),
    path('accptag/<int:aid>',views.accptag,name="AcceptAgency"),
    path('rjctag/<int:rid>',views.rjctag,name="RejectAgency"),
    path('acptag/',views.AcptAg,name="AcceptedAgencies"),
    path('rjctag/',views.RjctAg,name="RejectedAgencies"),
    path('nwusrlst/',views.NwUsrLst,name="NewUserList"),
    path('cmplnt/',views.Cmplnt,name="Complaints"),
    path('reply/<int:rid>',views.Reply,name="Reply"),
]
