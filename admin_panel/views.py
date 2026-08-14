from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,"admin_templates/admin_dashboard.html")
def register_storage(request):
    return render(request,"admin_templates/storage_register.html")