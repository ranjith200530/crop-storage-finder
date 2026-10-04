from django.db import models
from django.contrib.auth.models import User







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