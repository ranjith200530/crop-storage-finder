from django.urls import path
from . import views
urlpatterns = [
    path('crop/',views.crop_listing,name="crop_listing"),

]