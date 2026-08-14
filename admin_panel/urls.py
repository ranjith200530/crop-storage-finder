from django.urls import path
from . import views
urlpatterns = [
    path('admin_home/',views.home,name="admin_home"),
    path('storage_register/',views.register_storage,name="storage_register"),
]