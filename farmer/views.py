
from django.shortcuts import render, redirect,get_object_or_404
from .models import FarmerCropListing
from buyer.models import BuyerCropRequirement
from accounts.models import State, District, SubDistrict


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
        "buyer/edit_crop_requirement.html",
        {
            "listing": listing
        }
    )
    
def delete_requirement(request, id):

    requirement = get_object_or_404(
        FarmerCropListing,
        id=id,
        user=request.user
    )

    requirement.delete()

    return redirect("my_crop_listings")