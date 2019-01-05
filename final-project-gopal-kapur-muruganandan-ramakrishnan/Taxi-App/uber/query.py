"""
Contains all the queries needed to get rides
"""
from datetime import timedelta
from .models import Ride

MAXIMUM_RIDES = 10
DECIMAL_LIMIT_FORMAT = "{0:.3f}"


def get_rides(latitude_threshold, longitude_threshold, time_threshold,
              latitude, longitude, time):
    latitude_lb = float(DECIMAL_LIMIT_FORMAT.format(latitude - latitude_threshold))
    latitude_ub = float(DECIMAL_LIMIT_FORMAT.format(latitude + latitude_threshold))
    longitude_lb = float(DECIMAL_LIMIT_FORMAT.format(longitude - longitude_threshold))
    longitude_ub = float(DECIMAL_LIMIT_FORMAT.format(longitude + longitude_threshold))

    rides = Ride.objects.filter(pickup_latitude__gte=latitude_lb,
                                pickup_latitude__lte=latitude_ub,
                                pickup_longitude__gte=longitude_lb,
                                pickup_longitude__lte=longitude_ub,
                                pickup_datetime__gte=time,
                                pickup_datetime__lte=time + timedelta(minutes=time_threshold))\
        .order_by("pickup_datetime")

    return rides[:MAXIMUM_RIDES]
