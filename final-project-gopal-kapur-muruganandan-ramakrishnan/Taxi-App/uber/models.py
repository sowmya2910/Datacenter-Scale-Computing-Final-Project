from django.db import models


class Ride(models.Model):
    vendorid = models.PositiveIntegerField(default=1)
    pickup_datetime = models.DateTimeField()
    dropoff_datetime = models.DateTimeField()
    rate_code = models.PositiveIntegerField(default=1)
    pickup_longitude = models.FloatField()
    pickup_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    passenger_count = models.IntegerField(default=1)
    trip_distance = models.FloatField()
    fare_amount = models.FloatField()
    tip_amount = models.FloatField()
    total_amount = models.FloatField()
    payment_type = models.PositiveIntegerField()
