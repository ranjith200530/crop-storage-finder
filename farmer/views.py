
from django.shortcuts import render, redirect,get_object_or_404
from .models import FarmerCropListing
from buyer.models import BuyerCropRequirement
from accounts.models import State, District, SubDistrict
from decimal import Decimal
from admin_panel.models import Storage
import requests
from django.conf import settings

def crop_listing(request):

    if request.method == "POST":

        # Get form data
        full_name=request.POST.get("Fullname")
        contact_number=request.POST.get("Contact")
        crop_name = request.POST.get("crop_name")

        quantity = request.POST.get("quantity")
        quantity_unit = request.POST.get("quantity_unit")

        price = request.POST.get("price")
        price_unit = request.POST.get("price_unit")


        # Get selected location IDs
        state_id = request.POST.get("state")
        district_id = request.POST.get("district")
        subdistrict_id = request.POST.get("sub_district")


        # Convert IDs into model objects
        state = State.objects.get(id=state_id)
        district = District.objects.get(id=district_id)
        subdistrict = SubDistrict.objects.get(id=subdistrict_id)


        # Save crop listing
        FarmerCropListing.objects.create(
            full_name=full_name,
            contact_number=contact_number,
            user=request.user,

            crop_name=crop_name,

            quantity=quantity,
            quantity_unit=quantity_unit,

            price=price,
            price_unit=price_unit,

            state=state,
            district=district,
            subdistrict=subdistrict
        )


        return redirect("farmer")


    # GET request
    states = State.objects.all()

    return render(
        request,
        "farmer/crop_listing.html",
        {
            "states": states
        }
    )
    
    
def my_crop_listings(request):

    listings = FarmerCropListing.objects.filter(
        user=request.user
    )

    return render(
        request,
        "farmer/my_crop_listings.html",
        {
            "listings": listings
        }
    )



def find_buyers(request, id):

    # Get farmer's crop listing
    listing = get_object_or_404(
        FarmerCropListing,
        id=id,
        user=request.user
    )

    # First priority: Same subdistrict
    buyers = BuyerCropRequirement.objects.filter(
        crop_name=listing.crop_name,
        subdistrict=listing.subdistrict
    )

    # If no buyers found, search district level
    if not buyers.exists():

        buyers = BuyerCropRequirement.objects.filter(
            crop_name=listing.crop_name,
            district=listing.district
        )

    return render(
        request,
        "farmer/buyer_results.html",
        {
            "listing": listing,
            "buyers": buyers
        }
    )



def edit_farmer_crop(request, id):

    listing = get_object_or_404(
        FarmerCropListing,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        listing.quantity = request.POST.get("quantity")
        listing.quantity_unit = request.POST.get("quantity_unit")

        listing.price = request.POST.get("price")
        listing.price_unit = request.POST.get("price_unit")

        listing.save()

        return redirect("my_crop_listings")

    return render(
        request,
        "farmer/edit_farmer_crop.html",
        {
            "listing": listing
        }
    )
    
def delete_farmer_requirement(request, id):

    requirement = get_object_or_404(
        FarmerCropListing,
        id=id,
        user=request.user
    )

    requirement.delete()

    return redirect("my_crop_listings")





# def find_storage(request):
#     states=State.objects.all()
#     if request.method == "POST":

#         # =====================================================
#         # 1. FARMER DETAILS
#         # =====================================================

#         name = request.POST.get("name")
#         mobile = request.POST.get("mobile")

#         # =====================================================
#         # 2. CROP DETAILS
#         # =====================================================

#         crop_name = request.POST.get("crop_name")
#         quantity = Decimal(request.POST.get("quantity"))
#         quantity_unit = request.POST.get("quantity_unit")

#         # =====================================================
#         # 3. LOCATION DETAILS
#         # =====================================================

#         state_id = request.POST.get("state")
#         district_id = request.POST.get("district")
#         subdistrict_id = request.POST.get("sub_district")

#         state = State.objects.get(id=state_id)
#         district = District.objects.get(id=district_id)
#         subdistrict = SubDistrict.objects.get(id=subdistrict_id)

#         # =====================================================
#         # 4. CONVERT FARMER QUANTITY TO KG
#         # =====================================================

#         if quantity_unit == "Kg":

#             required_kg = quantity

#         elif quantity_unit == "Quintal":

#             required_kg = quantity * Decimal("100")

#         elif quantity_unit == "Ton":

#             required_kg = quantity * Decimal("1000")

#         else:

#             required_kg = quantity

#         # =====================================================
#         # 5. RECOMMEND STORAGE TYPE BASED ON CROP
#         # =====================================================

#         crop = crop_name.lower().strip()

#         warehouse_crops = [
#             "paddy",
#             "rice",
#             "wheat",
#             "maize",
#             "corn",
#             "millet",
#             "bajra",
#             "jowar",
#             "barley",
#             "pulses",
#             "gram",
#             "chickpea",
#         ]

#         cold_storage_crops = [
#             "potato",
#             "tomato",
#             "onion",
#             "carrot",
#             "cabbage",
#             "cauliflower",
#             "peas",
#             "apple",
#             "orange",
#             "grapes",
#             "mango",
#             "banana",
#             "vegetables",
#             "fruits",
#         ]

#         if crop in warehouse_crops:

#             recommended_type = "warehouse"

#         elif crop in cold_storage_crops:

#             recommended_type = "cold_storage"

#         else:

#             recommended_type = None

#         # =====================================================
#         # 6. FUNCTION TO CHECK AVAILABLE CAPACITY
#         # =====================================================

#         def has_capacity(storage):

#             if storage.capacity_unit == "Kg":

#                 available_kg = storage.available_capacity

#             elif storage.capacity_unit == "Quintal":

#                 available_kg = (
#                     storage.available_capacity * Decimal("100")
#                 )

#             elif storage.capacity_unit == "Ton":

#                 available_kg = (
#                     storage.available_capacity * Decimal("1000")
#                 )

#             else:

#                 available_kg = storage.available_capacity

#             return available_kg >= required_kg

#         # =====================================================
#         # 7. SEARCH SUBDISTRICT FIRST
#         # =====================================================

#         suitable_storages = []

#         if recommended_type:

#             # Search only for the recommended storage type
#             storages = Storage.objects.filter(
#                 subdistrict=subdistrict,
#                 storage_type=recommended_type
#             )

#         else:

#             # If crop is unknown, search both storage types
#             storages = Storage.objects.filter(
#                 subdistrict=subdistrict
#             )

#         for storage in storages:

#             if has_capacity(storage):

#                 suitable_storages.append(storage)

#         location_level = "SubDistrict"

#         # =====================================================
#         # 8. IF NO SUITABLE STORAGE → SEARCH DISTRICT
#         # =====================================================

#         if not suitable_storages:

#             if recommended_type:

#                 storages = Storage.objects.filter(
#                     district=district,
#                     storage_type=recommended_type
#                 )

#             else:

#                 storages = Storage.objects.filter(
#                     district=district
#                 )

#             for storage in storages:

#                 if has_capacity(storage):

#                     suitable_storages.append(storage)

#             location_level = "District"

        

#         recommended_storages = []
#         other_storages = []

#         if recommended_type:

#             for storage in suitable_storages:

#                 if storage.storage_type == recommended_type:

#                     recommended_storages.append(storage)

#                 else:

#                     other_storages.append(storage)

#         else:

#             other_storages = suitable_storages

      

#         context = {

#             # Farmer details
#             "name": name,
#             "mobile": mobile,

#             # Crop details
#             "crop_name": crop_name,
#             "quantity": quantity,
#             "quantity_unit": quantity_unit,
#             "required_kg": required_kg,

#             # Location
#             "state": state,
#             "district": district,
#             "subdistrict": subdistrict,

#             # Search information
#             "location_level": location_level,

#             # Recommendation
#             "recommended_type": recommended_type,

#             # Results
#             "recommended_storages": recommended_storages,
#             "other_storages": other_storages,
#         }

#         return render(
#             request,
#             "farmer/nearby_storages.html",
#             context
#         )

    
#     return render(
#         request,
#         "farmer/storage_search_form.html",
#         {"states":states}
#     )
    
def find_storage(request):

    states = State.objects.all()
    
    if request.method == "POST":
        api_key = settings.GOOGLE_GEOCODING_API_KEY

        name = request.POST.get("name")
        mobile = request.POST.get("mobile")

        # =====================================================
        # 2. CROP DETAILS
        # =====================================================

        crop_name = request.POST.get("crop_name")
        quantity = Decimal(request.POST.get("quantity"))
        quantity_unit = request.POST.get("quantity_unit")

        # =====================================================
        # 3. LOCATION DETAILS
        # =====================================================

        state_id = request.POST.get("state")
        district_id = request.POST.get("district")
        subdistrict_id = request.POST.get("sub_district")
        address=request.POST.get("address")

        state = State.objects.get(id=state_id)
        district = District.objects.get(id=district_id)
        subdistrict = SubDistrict.objects.get(id=subdistrict_id)
        
        full_address = (
            f"{subdistrict.name}, "
            f"{district.name}, "
            f"{state.name}, "
            f"{address},"
            f"India"
             )

        url = "https://geocode.googleapis.com/v4/geocode/address"

        params = {
        "addressQuery": full_address,
        "key": api_key
         }

        response = requests.get(
          url,
         params=params,
         timeout=10
        )

        data = response.json()

        latitude = None
        longitude = None

        if response.status_code == 200:
            if data.get("results"):

                location = data["results"][0]["location"]

                latitude = location["latitude"]

                longitude = location["longitude"]

        # =====================================================
        # 4. CONVERT FARMER QUANTITY TO KG
        # =====================================================

        if quantity_unit == "Kg":

            required_kg = quantity

        elif quantity_unit == "Quintal":

            required_kg = (
                quantity * Decimal("100")
            )

        elif quantity_unit == "Ton":

            required_kg = (
                quantity * Decimal("1000")
            )

        elif quantity_unit == "MT":

            required_kg = (
                quantity * Decimal("1000")
            )

        else:

            required_kg = quantity

        # =====================================================
        # 5. RECOMMEND STORAGE TYPE BASED ON CROP
        # =====================================================

        crop = crop_name.lower().strip()

        warehouse_crops = [
            "paddy",
            "rice",
            "wheat",
            "maize",
            "corn",
            "millet",
            "bajra",
            "jowar",
            "barley",
            "pulses",
            "gram",
            "chickpea",
        ]

        cold_storage_crops = [
            "potato",
            "tomato",
            "onion",
            "carrot",
            "cabbage",
            "cauliflower",
            "peas",
            "apple",
            "orange",
            "grapes",
            "mango",
            "banana",
            "vegetables",
            "fruits",
        ]

        if crop in warehouse_crops:

            recommended_type = "warehouse"

        elif crop in cold_storage_crops:

            recommended_type = "cold_storage"

        else:

            recommended_type = None

        # =====================================================
        # 6. FUNCTION TO CHECK AVAILABLE CAPACITY
        # =====================================================

        def has_capacity(storage):

            # -------------------------------------------------
            # Storage capacity is stored in KG
            # -------------------------------------------------

            if storage.capacity_unit == "Kg":

                available_kg = (
                    storage.available_capacity
                )

            # -------------------------------------------------
            # 1 QUINTAL = 100 KG
            # -------------------------------------------------

            elif storage.capacity_unit == "Quintal":

                available_kg = (
                    storage.available_capacity
                    * Decimal("100")
                )

            # -------------------------------------------------
            # 1 TON = 1000 KG
            # -------------------------------------------------

            elif storage.capacity_unit == "Ton":

                available_kg = (
                    storage.available_capacity
                    * Decimal("1000")
                )

            # -------------------------------------------------
            # 1 MT = 1000 KG
            # -------------------------------------------------

            elif storage.capacity_unit == "MT":

                available_kg = (
                    storage.available_capacity
                    * Decimal("1000")
                )

            else:

                available_kg = (
                    storage.available_capacity
                )

            # -------------------------------------------------
            # Compare storage capacity with farmer requirement
            # -------------------------------------------------

            return available_kg >= required_kg

        # =====================================================
        # 7. SEARCH SUBDISTRICT FIRST
        # =====================================================

        suitable_storages = []

        if recommended_type:

            storages = Storage.objects.filter(
                subdistrict=subdistrict,
                storage_type=recommended_type
            )

        else:

            storages = Storage.objects.none()

        for storage in storages:

            if has_capacity(storage):

                suitable_storages.append(storage)

        location_level = "SubDistrict"

        # =====================================================
        # 8. IF NO SUITABLE STORAGE → SEARCH DISTRICT
        # =====================================================

        if not suitable_storages:

            if recommended_type:

                storages = Storage.objects.filter(
                    district=district,
                    storage_type=recommended_type
                )

            else:

                storages = Storage.objects.none()

            for storage in storages:

                if has_capacity(storage):

                    suitable_storages.append(storage)

            location_level = "District"

        # =====================================================
        # 9. ONLY RECOMMENDED STORAGES
        # =====================================================

        recommended_storages = suitable_storages

        # =====================================================
        # 10. GOOGLE PLACES API
        # =====================================================

        api_storages = []

        if recommended_type:

            # -------------------------------------------------
            # Create crop-specific Google search query
            # -------------------------------------------------

            if recommended_type == "warehouse":

                api_storage_type = "warehouse"

            elif recommended_type == "cold_storage":

                api_storage_type = "cold storage"

            else:

                api_storage_type = "storage"

            api_query = (
                f"{crop_name} {api_storage_type}"
            )

            # -------------------------------------------------
            # Google Places Text Search
            # -------------------------------------------------

            url = (
                "https://places.googleapis.com/"
                "v1/places:searchText"
            )

            headers = {

                "Content-Type": "application/json",

                "X-Goog-Api-Key":
                    api_key,

                "X-Goog-FieldMask": (
                    "places.id,"
                    "places.displayName,"
                    "places.formattedAddress,"
                    "places.internationalPhoneNumber,"
                    "places.location"
                )
            }

            # -------------------------------------------------
            # Location Bias
            # -------------------------------------------------

            data = { 
            "textQuery": api_query,
            "pageSize": 20,
            "regionCode": "IN",
            "locationRestriction": {
            "rectangle": { "low": {
            "latitude": latitude - 0.1,
            "longitude": longitude - 0.1
            
            },

            "high": {

                "latitude": latitude + 0.1,

                "longitude": longitude + 0.1
            
                                }
                            }
                    },
            
                    "rankPreference": "DISTANCE"
                }
    
 
            try:

                response = requests.post(
                    url,
                    headers=headers,
                    json=data,
                    timeout=10
                )

                google_data = response.json()

                # -------------------------------------------------
                # Check Google API Response
                # -------------------------------------------------

                if response.status_code == 200:

                    for place in google_data.get(
                        "places",
                        []
                    ):

                        name = place.get(
                            "displayName",
                            {}
                        ).get("text")

                        address = place.get(
                            "formattedAddress"
                        )

                        contact = place.get(
                            "internationalPhoneNumber"
                        )

                        place_id = place.get(
                            "id"
                        )

                        location = place.get(
                            "location",
                            {}
                        )

                        latitude = location.get(
                            "latitude"
                        )

                        longitude = location.get(
                            "longitude"
                        )

                        api_storage = {

                            "name": name,

                            "address": address,

                            "contact": contact,

                            "place_id": place_id,

                            "latitude": latitude,

                            "longitude": longitude,

                            "storage_type":
                                recommended_type,

                            "crop_name":
                                crop_name,
                        }

                        api_storages.append(
                            api_storage
                        )

                else:

                    print(
                        "Google Places API Error:",
                        google_data
                    )

            except requests.RequestException as e:

                print(
                    "Google Places API Request Error:",
                    e
                )

        # =====================================================
        # 11. CONTEXT
        # =====================================================

        context = {

            # Farmer details
            "name": name,
            "mobile": mobile,

            # Crop details
            "crop_name": crop_name,
            "quantity": quantity,
            "quantity_unit": quantity_unit,
            "required_kg": required_kg,

            # Location
            "state": state,
            "district": district,
            "subdistrict": subdistrict,

            # Search information
            "location_level": location_level,

            # Recommendation
            "recommended_type": recommended_type,

            # Results
            "recommended_storages":
                recommended_storages,

            # Google API Results
            "api_storages":
                api_storages,
        }

        return render(
            request,
            "farmer/nearby_storages.html",
            context
        )

    return render(
        request,
        "farmer/storage_search_form.html",
        {
            "states": states
        }
    )

