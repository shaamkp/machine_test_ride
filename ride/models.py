from django.db import models
from general.models import BaseModel


RIDE_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('accept', 'Accept'),
    ('cancelled', 'Cancelled'),
    ('completed', 'Completed')
)

class Ride(BaseModel):
    driver = models.ForeignKey("accounts.DriverProfile", on_delete=models.CASCADE, null=True, blank=True)
    rider = models.ForeignKey("accounts.RiderProfile", on_delete=models.CASCADE, null=True, blank=True)
    pick_up_location = models.TextField(null=True, blank=True)
    dropoff_location = models.TextField(null=True, blank=True)
    status = models.CharField(choices=RIDE_STATUS_CHOICES,max_length=20, default='pending')

    class Meta:
        db_table = 'ride_ride'
        verbose_name = 'ride'
        verbose_name_plural = 'rides'
        ordering = ('id',)

    def __str__(self):
        return self.pick_up_location
    

class RideLocation(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    date_added = models.DateTimeField(db_index=True,auto_now_add=True)

    def __str__(self):
        return f'Location for Ride #{self.ride.id}'

    class Meta:
        ordering = ['-timestamp']

