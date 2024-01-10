from django.db import models
from general.models import BaseModel


ACCOUNTS_DRIVER_PROFILE_STATUS_CHOICES = (
    ('available', 'Available'),
    ('busy', 'Busy')

)

class RiderProfile(BaseModel):
    name = models.CharField(max_length=125, null=True, blank=True)
    phone = models.CharField(max_length=125, null=True, blank=True)
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    password = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'accounts_rider_profile'
        verbose_name = 'rider profile'
        verbose_name_plural = 'rider profiles'
        ordering = ('id',)

    def __str__(self):
        return self.name
    

class DriverProfile(BaseModel):
    name = models.CharField(max_length=125, null=True, blank=True)
    phone = models.CharField(max_length=125, null=True, blank=True)
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    status = models.CharField(max_length=128, choices=ACCOUNTS_DRIVER_PROFILE_STATUS_CHOICES, null=True, blank=True) 
    password = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'accounts_driver_profile'
        verbose_name = 'driver profile'
        verbose_name_plural = 'driver profiles'
        ordering = ('id',)

    def __str__(self):
        return self.name
