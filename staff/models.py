# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from admin_panel.models import Storage

class BookingRequest(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    # -------------------------
    # Farmer
    # -------------------------

    farmer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="booking_requests"
    )

    farmer_name = models.CharField(
        max_length=150
    )

    mobile = models.CharField(
        max_length=10
    )

    # -------------------------
    # Crop details
    # -------------------------

    crop_name = models.CharField(
        max_length=100
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    quantity_unit = models.CharField(
        max_length=20
    )

    # -------------------------
    # Selected storage
    # -------------------------

    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        related_name="booking_requests"
    )

    # -------------------------
    # Booking status
    # -------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    # -------------------------
    # Request date/time
    # -------------------------

    requested_at = models.DateTimeField(
        auto_now_add=True
    )
    
    accepted_on = models.DateTimeField(
    null=True,
    blank=True
    )

    def __str__(self):
        return f"{self.farmer_name} - {self.storage.storage_name}"