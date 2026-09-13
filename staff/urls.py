from django.urls import path
from . import views


urlpatterns = [
path('booking_request',views.booking_request,name="booking_request"),
path('show_bookings/<int:id>/',views.staff_booking_requests,name="staff_booking_requests"),
   path(
        "update-booking-status/<int:id>/",
        views.update_booking_status,
        name="update_booking_status"
    ),
   path(
    "staff/accepted-bookings/<int:id>/",
    views.staff_accepted_bookings,
    name="staff_accepted_bookings"
),
path(
    "staff/remove-booking/<int:id>/",
    views.remove_booking,
    name="remove_booking"
),
path(
    "staff/calculate-charge/<int:id>/",
    views.calculate_charge,
    name="calculate_charge"
),
]