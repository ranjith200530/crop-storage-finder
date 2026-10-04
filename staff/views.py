
from django.shortcuts import redirect, get_object_or_404,render
from django.contrib.auth.decorators import login_required
from .models import BookingRequest
from admin_panel.models import Storage
from django.utils import timezone
from django.http import JsonResponse
from decimal import Decimal
from django.contrib import messages
from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect


def booking_request(request):

    if request.method == "POST":

      
        farmer_name = request.POST.get("farmer_name")
        mobile = request.POST.get("mobile")
        crop_name = request.POST.get("crop_name")
        quantity = request.POST.get("quantity")
        quantity_unit = request.POST.get("quantity_unit")
        storage_id = request.POST.get("storage_id")

        storage = get_object_or_404(
            Storage,
            id=storage_id
        )

    #saving the reuqest 
        BookingRequest.objects.create(
            farmer=request.user,
            farmer_name=farmer_name,
            mobile=mobile,
            crop_name=crop_name,
            quantity=quantity,
            quantity_unit=quantity_unit,
            storage=storage,
            status="pending"
        )
        messages.success(
            request,
            "Booking request successfully sent!"
        )
        # After successful booking
        return redirect("farmer")


def staff_booking_requests(request,id):

    storage = get_object_or_404(
        Storage,
        id=id,
    )

    booking_requests = BookingRequest.objects.filter(
        storage=storage,
        status="pending"
    )
    
  

    return render(
        request,
        "staff_templates/booking_requests.html",
        {
            "storage": storage,
            "booking_requests": booking_requests
        }
    )
    



def update_booking_status(request, id):

    booking = get_object_or_404(
        BookingRequest,
        id=id
    )

    if request.method == "POST":  

        status = request.POST.get("status")  

        if status == "accepted":  

            storage = booking.storage  
 

            available_mt = storage.available_capacity  

            if booking.quantity_unit == "Kg":

                required_kg = booking.quantity

            elif booking.quantity_unit == "Quintal":

                required_kg = (
                    booking.quantity * Decimal("100")
                )

            elif booking.quantity_unit == "Ton":

                required_kg = (
                    booking.quantity * Decimal("1000")
                )

            else:

                required_kg = booking.quantity


            # -----------------------------------
            # Convert farmer KG to MT
            # -----------------------------------

            required_mt = (
                required_kg / Decimal("1000")
            )

            if available_mt >= required_mt:

                # Reduce ONLY the quantity requested
                storage.available_capacity = (
                    available_mt - required_mt
                )
                if storage.available_capacity<1:
                    available_mt=storage.available_capacity*1000
                else:
                    available_mt=storage.available_capacity

                storage.save(
                    update_fields=["available_capacity"]
                )

                booking.status = "accepted"
                booking.accepted_on = timezone.now()

                booking.save(
                    update_fields=["status", "accepted_on"]
                )
                


            else:

                # Not enough storage
                booking.status = "rejected"

                booking.save(
                    update_fields=["status"]
                )


        elif status == "rejected":

            booking.status = "rejected"

            booking.save(
                update_fields=["status"]
            )

     
    return redirect(
        "staff_booking_requests",
        id=booking.storage.id
    )


    
    
def staff_accepted_bookings(request, id):

    storage = get_object_or_404(
        Storage,
        id=id
    )

    accepted_bookings = BookingRequest.objects.filter(
        storage=storage,
        status="accepted"
    )

    return render(
        request,
        "staff_templates/accepted_bookings.html",
        {
            "storage": storage,
            "bookings": accepted_bookings
        }
    )
    



def remove_booking(request, id):

    # Only POST request is allowed
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Invalid request."
        })

    # Get the booking
    booking = get_object_or_404(
        BookingRequest,
        id=id
    )

    # Only accepted bookings can be removed
    if booking.status != "accepted":
        return JsonResponse({
            "success": False,
            "message": "This booking is not accepted."
        })

    # Get the storage associated with this booking
    storage = booking.storage

    # Convert booking quantity to Metric Ton
    if booking.quantity_unit == "Kg":

        occupied_mt = booking.quantity / Decimal("1000")

    elif booking.quantity_unit == "Quintal":

        occupied_mt = booking.quantity / Decimal("10")

    elif booking.quantity_unit == "Ton":

        occupied_mt = booking.quantity

    else:
        return JsonResponse({
            "success": False,
            "message": "Invalid quantity unit."
        })

    # Release the occupied storage capacity
    storage.available_capacity += occupied_mt

    # Available capacity should never exceed total capacity
    if storage.available_capacity > storage.capacity:
        storage.available_capacity = storage.capacity

    # Save the updated storage capacity
    storage.save(
        update_fields=["available_capacity"]
    )

    # Booking is completed
    booking.status = "completed"

    booking.save(
        update_fields=["status"]
    )

    return JsonResponse({
        "success": True,
        "message": "Booking removed successfully."
    })


def calculate_charge(request, id):

    booking = get_object_or_404(
        BookingRequest,
        id=id
    )

    if booking.status != "accepted":

        return JsonResponse({
            "success": False,
            "message": "This booking is not accepted."
        })

    if booking.accepted_on is None:

        return JsonResponse({
            "success": False,
            "message": "Booking accepted date is missing."
        })


    if booking.quantity_unit == "Kg":

        quantity_kg = booking.quantity

    elif booking.quantity_unit == "Quintal":

        quantity_kg = (
            booking.quantity *
            Decimal("100")
        )

    elif booking.quantity_unit == "Ton":

        quantity_kg = (
            booking.quantity *
            Decimal("1000")
        )

    else:

        return JsonResponse({
            "success": False,
            "message": "Invalid quantity unit."
        })

    #calculating storage days

    today = timezone.localdate()

    accepted_date = booking.accepted_on.date()

    days = (
        today -
        accepted_date
    ).days + 1

   
    # Calculate monthly charge
    

    monthly_charge = (
        quantity_kg *
        booking.storage.price_per_kg
    )

  
    # Calculate daily charge
  

    daily_charge = (
        monthly_charge /
        Decimal("30")
    )

    
    # Calculate total charge
   

    total_charge = (
        daily_charge *
        Decimal(days)
    )



    return JsonResponse({

        "success": True,

        "days": days,

        "total_charge": float(
            total_charge
        )

    })