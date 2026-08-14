from django.urls import path
from . import views
urlpatterns = [
    path('crop/',views.crop_listing,name="crop_listing"),
    path('mycrops/',views.my_crop_listings,name="my_crop_listings"),
   path("edit_crop/<int:id>/",views.edit_farmer_crop,name="edit_farmer_crop"),
   path("delete_crop/<int:id>/",views.delete_requirement,name="delete_crop"),
   path("find_buyers/<int:id>/",views.find_buyers,name="find_buyers"),
]