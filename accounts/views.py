from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group

from django.contrib.auth import authenticate,login,logout
from . import models

import re
from django.contrib import messages
# Create your views here.

def buyer(req):
    return render(req,"buyer/buyer_dashborad.html")
def farmer(req):
    return render(req,"farmer/farmer_dashboard.html")

def login_view(request):

    # If user is already logged in
    if request.user.is_authenticated:

        if request.user.groups.filter(name="Farmer").exists():
            return redirect("farmer")

        elif request.user.groups.filter(name="Buyer").exists():
            return redirect("buyer")

    


    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")


        # Empty field validation
        if not username:
            messages.error(request,"Please Enter User Name")
        if not password:
            messages.error(request,"Please Enter Password")

        # Authenticate user
        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is None:
            messages.error(request, "Invalid Username or Password.")
            return redirect("login")


        # Login user
        login(request, user)


        # Redirect according to group
        if user.groups.filter(name="Farmer").exists():
            return redirect("farmer")


        elif user.groups.filter(name="Buyer").exists():
            return redirect("buyer")




    return render(request, "accounts/login_page.html")



def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")
        if username == "":
            messages.error(request, "Username is required")
            return redirect("register")

        if password == "":
            messages.error(request, "Password is required")
            return redirect("register")

        if confirm_password == "":
            messages.error(request, "Confirm password is required")
            return redirect("register")

        if role == "":
            messages.error(request, "Please select a role")
            return redirect("register")

        # Username validation
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")


        # Password match validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")
        if len(password) < 8:
            messages.error(request, "Password must contain at least 8 characters")
            return redirect("register")
        if not re.search(r"[A-Z]", password):
            messages.error(request, "Password must contain at least one uppercase letter (A-Z)")
            return redirect("register")


        if not re.search(r"[a-z]", password):
            messages.error(request, "Password must contain at least one lowercase letter (a-z)")
            return redirect("register")


        if not re.search(r"[0-9]", password):
            messages.error(request, "Password must contain at least one number (0-9)")
            return redirect("register")


        if not re.search(r"[@#$%^&+=]", password):
            messages.error(request, "Password must contain at least one special character (@#$%^&+=)")
            return redirect("register")


       
       

        # Create User
        user = User.objects.create_user(
            username=username,
            password=password,
        )
        

        # Add user to respective group
        group = Group.objects.get(name=role)
        user.groups.add(group)


        messages.success(request, "Registration successful")

        return redirect("login")


    return render(request, "accounts/register_page.html")

def logout_view(request):
    logout(request)
    return redirect("login")


# locations/views.py

from django.http import JsonResponse
from .models import District, SubDistrict


def load_districts(request):

    state_id = request.GET.get("state_id")

    districts = District.objects.filter(state_id=state_id).values(
        "id",
        "name"
    )

    return JsonResponse(list(districts), safe=False)


def load_subdistricts(request):

    district_id = request.GET.get("district_id")

    subdistricts = SubDistrict.objects.filter(
        district_id=district_id
    ).values(
        "id",
        "name"
    )

    return JsonResponse(list(subdistricts), safe=False)