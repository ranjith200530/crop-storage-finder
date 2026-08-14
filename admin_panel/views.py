from django.shortcuts import render, redirect, get_object_or_404
from .models import Storage
from accounts.models import State, District, SubDistrict
import requests
from django.conf import settings


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