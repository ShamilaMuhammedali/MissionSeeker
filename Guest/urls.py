from django.urls import path
from Guest import views
app_name='guest'

urlpatterns = [
    path('home/',views.home,name="Home"),
    path('newuser/',views.newuser,name="Newuser"),
    path('ajax_place/',views.ajaxplace,name="Ajax_Place"),
    path('login/',views.login,name="Login"),
    path('newagency/',views.newagency,name="NewAgency"),
]