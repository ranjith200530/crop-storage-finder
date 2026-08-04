from django.urls import path
from . import views
urlpatterns = [
    path('crop/',views.crop_listing,name="crop_listing"),
    path('mycrops/',views.my_crop_listings,name="my_crop_listings"),

]