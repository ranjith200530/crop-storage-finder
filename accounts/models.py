from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(
        max_length=100
    )

    contact_number = models.CharField(
        max_length=10
    )

    state = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
  

    district = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )


    def __str__(self):
        return self.full_name
    



class State(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class District(models.Model):
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name="districts"
    )

    name = models.CharField(max_length=150)

    class Meta:
        unique_together = ('state', 'name')

    def __str__(self):
        return self.name


class SubDistrict(models.Model):
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name="subdistricts"
    )

    name = models.CharField(max_length=150)

    class Meta:
        unique_together = ('district', 'name')

    def __str__(self):
        return self.name