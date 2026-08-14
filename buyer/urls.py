from django.urls import path
from . import views
urlpatterns = [
    path('requirement/',views.requiremnt_listing,name="requirement_listing"),
    path('myrequirement/',views.my_requirements,name="my_requirements"),
path("find-farmers/<int:requirement_id>/",views.find_farmers,name="find_farmers"),
path("edit_crop/<int:id>/",views.edit_crop_requirement,name="edit_requirement"),
path("delete_crop/<int:id>/",views.delete_requirement,name="delete_requirement"),
]