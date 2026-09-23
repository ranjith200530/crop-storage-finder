from django.urls import path
from . import views
urlpatterns = [
    path('admin_home/',views.home,name="admin_home"),
    path('storage_register/',views.register_storage,name="storage_register"),
    path("create/",views.create_staff,name="create_staff"),
    path("show-storage-staff/<int:id>/",views.show_my_staff,name="show_my_staff"),  
    path("show-all-storages/",views.show_storages,name="show-storages"),
   path(
    "delete-staff/<int:id>/",
    views.delete_staff,
    name="delete_staff"
),
]