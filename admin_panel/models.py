from django.db import models

# Create your models here.
from django.db import models
from accounts.models import SubDistrict,State,District


class Storage(models.Model):

    # =========================
    # STORAGE INFORMATION
    # =========================

    storage_name = models.CharField(
        max_length=200
    )

    storage_type = models.CharField(
        max_length=50,
        choices=[
            ("cold_storage", "Cold Storage"),
            ("warehouse", "Warehouse"),
        ]
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
        choices=[
            ("kg", "Kg"),
            ("quintal", "Quintal"),
            ("ton", "Ton"),
        ]
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