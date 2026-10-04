from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,Group

from django.contrib.auth import authenticate,login,logout
from . import models
from admin_panel.models import StaffAssignment
import re
from django.contrib import messages
from django.http import JsonResponse
from .models import District, SubDistrict

# Create your views here.

def buyer(req):
    user = req.user
    full_name = user.first_name + " " + user.last_name
    return render(req,"buyer/buyer_dashborad.html",{"user":full_name})
def farmer(req):
    user = req.user
    full_name = user.first_name + " " + user.last_name
    return render(req,"farmer/farmer_dashboard.html",{"user":full_name})


def staff(request):

    staff_assignment = StaffAssignment.objects.get(
        user=request.user
    )
    user=request.user
    full_name= user.first_name + " " + user.last_name
 
    storage = staff_assignment.storage

    return render(
        request,
        "staff_templates/staff_home.html",
        {
            "storage": storage,
            "user":full_name
        }
    )


def login_view(request):

    # If user is already logged in
    if request.user.is_authenticated:

        # Superuser
        if request.user.is_superuser:
            return redirect("admin_home")

        # Farmer
        if request.user.groups.filter(name="Farmer").exists():
            return redirect("farmer")

        # Storage Staff
        if request.user.groups.filter(name="Storage_staff").exists():
            return redirect("staff_dashboard")

        # Buyer
        elif request.user.groups.filter(name="Buyer").exists():
            return redirect("buyer")


    if request.method == "POST":

        # Template uses name="username",
        # but the user enters their email
        username = request.POST.get("username")
        password = request.POST.get("password")


        # Empty field validation
        if not username:
            messages.error(request, "Please Enter Email")
            return redirect("login")

        if not password:
            messages.error(request, "Please Enter Password")
            return redirect("login")


        # Authenticate user
        # username contains the email
        user = authenticate(
            request,
            username=username,
            password=password
        )

        # Invalid email or password
        if user is None:
            messages.error(request, "Invalid Email or Password.")
            return redirect("login")

        # Login user
        login(request, user)

        # Redirect according to user type

        # Superuser
        if user.is_superuser:
            return redirect("admin_home")

        # Farmer
        elif user.groups.filter(name="Farmer").exists():
            return redirect("farmer")

        # Storage Staff
        elif user.groups.filter(name="Storage_staff").exists():
            return redirect("staff_dashboard")

        # Buyer
        elif user.groups.filter(name="Buyer").exists():
            return redirect("buyer")


    return render(request, "accounts/login_page.html")


def register(request):

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")


        # Required field validation

        if first_name == "":
            messages.error(request, "First name is required")
            return redirect("register")


        if last_name == "":
            messages.error(request, "Last name is required")
            return redirect("register")


        if email == "":
            messages.error(request, "Email is required")
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


        # Email validation
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("register")


        # Password match validation

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")


        if len(password) < 8:
            messages.error(
                request,
                "Password must contain at least 8 characters"
            )
            return redirect("register")


        if not re.search(r"[A-Z]", password):
            messages.error(
                request,
                "Password must contain at least one uppercase letter (A-Z)"
            )
            return redirect("register")


        if not re.search(r"[a-z]", password):
            messages.error(
                request,
                "Password must contain at least one lowercase letter (a-z)"
            )
            return redirect("register")


        if not re.search(r"[0-9]", password):
            messages.error(
                request,
                "Password must contain at least one number (0-9)"
            )
            return redirect("register")


        if not re.search(r"[@#$%^&+=]", password):
            messages.error(
                request,
                "Password must contain at least one special character (@#$%^&+=)"
            )
            return redirect("register")


        # Create User

        user = User.objects.create_user(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )


        # Add user to respective group

        group = Group.objects.get(name=role)
        user.groups.add(group)

        login(request, user)


# Redirect according to group

        if user.groups.filter(name="Farmer").exists():
            messages.success(
             request,
            "Registration successful! Welcome to the Farmer Dashboard."
            )
            return redirect("farmer")

 
        elif user.groups.filter(name="Buyer").exists():
            messages.success(
           request,
        "Registration successful! Welcome to the Buyer Dashboard."
         )
            return redirect("buyer")




    return render(request, "accounts/register_page.html")




def logout_view(request):
    logout(request)
    return redirect("login")

def forgot_password(request):

    if request.method == "POST":

        username = request.POST.get("username")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")


        # Check passwords
        if new_password != confirm_password:

            messages.error(request, "Passwords do not match.")

            return redirect("forgot_password")

        # Find user using username
        try:

            user = User.objects.get(username=username)

        except User.DoesNotExist:

            messages.error(request, "No account found with this username.")

            return redirect("forgot_password")


        # Change password
        user.set_password(new_password)

        user.save()

        messages.success(
            request,
            "Password changed successfully. Please login."
        )

        return redirect("login")


    return render(request, "accounts/forgot_password.html")

# locations/views.py




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