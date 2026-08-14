
from django.shortcuts import render, redirect
from .models import BuyerCropRequirement
from accounts.models import State, District, SubDistrict
from django.shortcuts import render, get_object_or_404
from farmer.models import FarmerCropListing


def requiremnt_listing(request):

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
        BuyerCropRequirement.objects.create(
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


        return redirect("buyer")


    # GET request
    states = State.objects.all()

    return render(
        request,
        "farmer/crop_listing.html",
        {
            "states": states
        }
    )


def my_requirements(request):

    requirements = BuyerCropRequirement.objects.filter(
        user=request.user
    )

    return render(
        request,
        "buyer/my_requirements.html",
        {
            "requirements": requirements
        }
    )
    
    





def find_farmers(request, requirement_id):

    # Get buyer requirement
    requirement = get_object_or_404(
        BuyerCropRequirement,
        id=requirement_id,
        user=request.user
    )


    # First priority: Same subdistrict
    farmers = FarmerCropListing.objects.filter(
        crop_name=requirement.crop_name,
        subdistrict=requirement.subdistrict
    )


    # If no farmers found, search district level
    if not farmers.exists():

        farmers = FarmerCropListing.objects.filter(
            crop_name=requirement.crop_name,
            district=requirement.district
        )


    


    return render(
        request,
        "buyer/farmer_results.html",
        {
            "requirement": requirement,
            "farmers": farmers
        }
    )
    


def edit_crop_requirement(request, id):

    listing = get_object_or_404(
        BuyerCropRequirement,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        listing.quantity = request.POST.get("quantity")
        listing.quantity_unit = request.POST.get("quantity_unit")

        listing.price = request.POST.get("price")
        listing.price_unit = request.POST.get("price_unit")

        listing.save()

        return redirect("my_requirements")

    return render(
        request,
        "buyer/edit_crop_requirement.html",
        {
            "listing": listing
        }
    )
    
def delete_requirement(request, id):

    requirement = get_object_or_404(
        BuyerCropRequirement,
        id=id,
        user=request.user
    )

    requirement.delete()

    return redirect("my_requirements")