from django.db import models

# Create your models here.
from accounts.models import SubDistrict,State,District
from django.contrib.auth.models import User


class Storage(models.Model):

    # =========================
    # STORAGE INFORMATION
    # =========================

    storage_name = models.CharField(
        max_length=200
    )

    storage_type = models.CharField(
        max_length=50,
    )

    # =========================
    # CAPACITY
    # =========================

    capacity = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    capacity_unit = models.CharField(
        max_length=20,
    )
    available_capacity = models.DecimalField(
    max_digits=12,
    decimal_places=2
)
    # =========================
    # STORAGE CHARGE
    # =========================

    # Storage charge is ₹ per kg per month
    price_per_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # =========================
    # LOCATION
    # =========================

    # SubDistrict already points to:
    # SubDistrict → District → State

    state = models.ForeignKey(
            State,
            on_delete=models.PROTECT
        )
    
    district = models.ForeignKey(
            District,
            on_delete=models.PROTECT
        )
    
    subdistrict = models.ForeignKey(
            SubDistrict,
            on_delete=models.PROTECT
        )
    

    # Complete local address
    address = models.TextField()

    # =========================
    # COORDINATES
    # =========================

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    # =========================
    # CONTACT INFORMATION
    # =========================

    main_contact_number = models.CharField(
        max_length=15
    )

    additional_contact_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    # =========================
    # TIMESTAMPS
    # =========================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =========================
    # DISPLAY
    # =========================

    def __str__(self):
        return self.storage_name
    
    
    



class StaffAssignment(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="staff_assignment"
    )

    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        related_name="staff_members"
    )

    def __str__(self):
        return f"{self.user.username} - {self.storage.storage_name}"