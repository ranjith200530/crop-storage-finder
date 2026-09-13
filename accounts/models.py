from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    username = models.CharField(
        max_length=150
    )

    role = models.CharField(
        max_length=20
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'role'],
                name='unique_username_per_role'
            )
        ]

    def __str__(self):
        return f"{self.username} - {self.role}"
    



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