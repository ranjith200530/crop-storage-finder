import re
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import State, District, SubDistrict
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User,Group
from .models import Storage, StaffAssignment
from django.db.models import Count
from django.db import transaction
from django.http import JsonResponse





# Create your views here.
def home(request):
    return render(request,"admin_templates/admin_dashboard.html")





def register_storage(request):
    states=State.objects.all()
    if request.method == "POST":

        storage_name = request.POST.get("storage_name")
        storage_type = request.POST.get("storage_type")

        capacity = request.POST.get("capacity")
        capacity_unit = request.POST.get("capacity_unit")

        price_per_kg = request.POST.get("price_per_kg")

        state_id = request.POST.get("state")
        district_id = request.POST.get("district")
        subdistrict_id = request.POST.get("sub_district")

        address = request.POST.get("address")

        main_contact_number = request.POST.get(
            "main_contact_number"
        )

        additional_contact_number = request.POST.get(
            "additional_contact_number"
        )


        # -----------------------------------
        # GET STATE, DISTRICT, SUBDISTRICT
        # -----------------------------------

        state = get_object_or_404(
            State,
            id=state_id
        )

        district = get_object_or_404(
            District,
            id=district_id
        )

        subdistrict = get_object_or_404(
            SubDistrict,
            id=subdistrict_id
        )
        full_address = f"{address},{subdistrict.name}, {district.name}, {state.name}, India"


        api_key = settings.GOOGLE_GEOCODING_API_KEY

        url = "https://geocode.googleapis.com/v4/geocode/address"
        params = {
            "addressQuery": full_address,
            "key": api_key
        }

        response = requests.get(
            url,
            params=params
        )
        
        data = response.json()
        

        # -----------------------------------
        # GET LATITUDE AND LONGITUDE
        # -----------------------------------

        latitude = None
        longitude = None

        if data:

            location = data["results"][0]["location"]

            latitude = location["latitude"]
            longitude = location["longitude"]


        # -----------------------------------
        # SAVE STORAGE
        # -----------------------------------

        Storage.objects.create(

            storage_name=storage_name,

            storage_type=storage_type,

            capacity=capacity,
            available_capacity=capacity,

            capacity_unit=capacity_unit,

            price_per_kg=price_per_kg,

            state=state,

            district=district,

            subdistrict=subdistrict,

            address=address,

            latitude=latitude,

            longitude=longitude,

            main_contact_number=main_contact_number,

            additional_contact_number=additional_contact_number
        )


        return redirect("admin_home")


    return render(
        request,
        "admin_templates/storage_register.html",{"states":states}
    )
    
# def show_storages(request):
#     data=Storage.objects.all()
#     return render(request,"admin_templates/all_storages.html",{"data":data})






# def create_staff(request):

#     # Get all storages
#     storages = Storage.objects.all()

#     if request.method == "POST":

#         username = request.POST.get("username", "").strip()
#         password = request.POST.get("password", "")
#         confirm_password = request.POST.get("confirm_password", "")
#         storage_id = request.POST.get("storage", "")

#         # Username required
#         if username == "":
#             messages.error(request, "Username is required")
#             return redirect("create_staff")

#         # Password required
#         if password == "":
#             messages.error(request, "Password is required")
#             return redirect("create_staff")

#         # Confirm password required
#         if confirm_password == "":
#             messages.error(request, "Confirm password is required")
#             return redirect("create_staff")

#         # Storage required
#         if storage_id == "":
#             messages.error(request, "Please select a storage")
#             return redirect("create_staff")

#         # Username already exists
#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists")
#             return redirect("create_staff")

#         # Passwords must match
#         if password != confirm_password:
#             messages.error(request, "Passwords do not match")
#             return redirect("create_staff")

#         # Password length
#         if len(password) < 8:
#             messages.error(
#                 request,
#                 "Password must contain at least 8 characters"
#             )
#             return redirect("create_staff")

#         # Uppercase
#         if not re.search(r"[A-Z]", password):
#             messages.error(
#                 request,
#                 "Password must contain at least one uppercase letter (A-Z)"
#             )
#             return redirect("create_staff")

#         # Lowercase
#         if not re.search(r"[a-z]", password):
#             messages.error(
#                 request,
#                 "Password must contain at least one lowercase letter (a-z)"
#             )
#             return redirect("create_staff")

#         # Number
#         if not re.search(r"[0-9]", password):
#             messages.error(
#                 request,
#                 "Password must contain at least one number (0-9)"
#             )
#             return redirect("create_staff")

#         # Special character
#         if not re.search(r"[@#$%^&+=]", password):
#             messages.error(
#                 request,
#                 "Password must contain at least one special character (@#$%^&+=)"
#             )
#             return redirect("create_staff")

#         # Get selected storage
#         storage = Storage.objects.get(id=storage_id)

#         # Create staff user
#         staff = User.objects.create_user(
#             username=username,
#             password=password
#         )

#         # Make user a staff member
#         staff.is_staff = True
#         staff.save()
#         storage_staff_group = Group.objects.get(name="Storage_staff")
#         staff.groups.add(storage_staff_group)
 
#         # Assign staff to storage
#         StaffAssignment.objects.create(
#             user=staff,
#             storage=storage
#         )

#         messages.success(
#             request,
#             "Staff account created and assigned to storage successfully."
#         )

#         return redirect("admin_home")

#     return render(
#         request,
#         "admin_templates/staff_assignment.html",
#         {
#             "storages": storages
#         }
#     )

def create_staff(request):

    # Get all storages
    storages = Storage.objects.all()

    if request.method == "POST":

        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()

        # username field in template contains email
        username = request.POST.get("username", "").strip()

        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        storage_id = request.POST.get("storage", "")

        # First name required
        if first_name == "":
            messages.error(request, "First name is required")
            return redirect("create_staff")

        # Last name required
        if last_name == "":
            messages.error(request, "Last name is required")
            return redirect("create_staff")

        # Email required
        if username == "":
            messages.error(request, "Email is required")
            return redirect("create_staff")

        # Password required
        if password == "":
            messages.error(request, "Password is required")
            return redirect("create_staff")

        # Confirm password required
        if confirm_password == "":
            messages.error(request, "Confirm password is required")
            return redirect("create_staff")

        # Storage required
        if storage_id == "":
            messages.error(request, "Please select a storage")
            return redirect("create_staff")

        # Email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Email already exists")
            return redirect("create_staff")

        # Passwords must match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("create_staff")

        # Password length
        if len(password) < 8:
            messages.error(
                request,
                "Password must contain at least 8 characters"
            )
            return redirect("create_staff")

        # Uppercase
        if not re.search(r"[A-Z]", password):
            messages.error(
                request,
                "Password must contain at least one uppercase letter (A-Z)"
            )
            return redirect("create_staff")

        # Lowercase
        if not re.search(r"[a-z]", password):
            messages.error(
                request,
                "Password must contain at least one lowercase letter (a-z)"
            )
            return redirect("create_staff")

        # Number
        if not re.search(r"[0-9]", password):
            messages.error(
                request,
                "Password must contain at least one number (0-9)"
            )
            return redirect("create_staff")

        # Special character
        if not re.search(r"[@#$%^&+=]", password):
            messages.error(
                request,
                "Password must contain at least one special character (@#$%^&+=)"
            )
            return redirect("create_staff")

        # Get selected storage
        storage = Storage.objects.get(id=storage_id)

        # Create staff user
        staff = User.objects.create_user(
            username=username,       # email is used as username
            first_name=first_name,
            last_name=last_name,
            email=username,          # actual email
            password=password
        )

        # Make user a staff member
        staff.is_staff = True
        staff.save()

        # Add Storage_staff group
        storage_staff_group = Group.objects.get(name="Storage_staff")
        staff.groups.add(storage_staff_group)

        # Assign staff to storage
        StaffAssignment.objects.create(
            user=staff,
            storage=storage
        )

        messages.success(
            request,
            "Staff account created and assigned to storage successfully."
        )

        return redirect("admin_home")

    return render(
        request,
        "admin_templates/staff_assignment.html",
        {
            "storages": storages
        }
    )
    
# def show_my_staff(request):

#     staff_members = StaffAssignment.objects.all()

#     return render(
#         request,
#         "admin_templates/my_staff.html",
#         {
#             "staff_members": staff_members
#         }
#     )


def show_storages(request):

    storages = Storage.objects.annotate(
        staff_count=Count("staff_members")
    )

    return render(
        request,
        "admin_templates/all_storages.html",
        {
            "storages": storages
        }
    )


def show_my_staff(request, id):

    storage = get_object_or_404(
        Storage,
        id=id
    )

    staff_members = StaffAssignment.objects.filter(
        storage=storage
    ).select_related("user")

    return render(
        request,
        "admin_templates/my_staff.html",
        {
            "storage": storage,
            "staff_members": staff_members
        }
    )
    
    



def delete_staff(request, id):

    if request.method != "POST":

        return JsonResponse(
            {
                "success": False,
                "message": "Invalid request method."
            },
            status=400
        )


    staff = get_object_or_404(
        StaffAssignment,
        user__id=id
    )


    user = staff.user


    with transaction.atomic():

       

        staff.delete()


        

        user.delete()


    return JsonResponse(
        {
            "success": True,
            "message": "Staff member deleted successfully."
        }
    )