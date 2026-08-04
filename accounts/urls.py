
from django.urls import path
from . import views
urlpatterns = [
    path('',views.login_view, name="login"),
    path('register/',views.register,name="register"),
    path('farmer/',views.farmer,name="farmer"),
    path('buyer/',views.buyer,name="buyer"),
     path("logout/", views.logout_view, name="logout"),
    
    path("ajax/load-districts/", views.load_districts, name="load_districts"),
    path("ajax/load-subdistricts/", views.load_subdistricts, name="load_subdistricts"),

]