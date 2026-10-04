from django.db import models
from django.contrib.auth.models import User
from accounts.models import State, District, SubDistrict


class BuyerCropRequirement(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    crop_name = models.CharField(
        max_length=100
    )

    quantity = models.FloatField()

    quantity_unit = models.CharField(
        max_length=20,
       
    )


    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    price_unit = models.CharField(
        max_length=20,
    
    )


    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE
    )

    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE
    )

    subdistrict = models.ForeignKey(
        SubDistrict,
        on_delete=models.CASCADE
    )
    
    full_name = models.CharField(
        max_length=100
    )

    contact_number = models.CharField(
        max_length=15
    )



    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.crop_name} - {self.user.username}"