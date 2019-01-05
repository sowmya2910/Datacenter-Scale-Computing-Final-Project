import datetime
import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

from .query import get_rides
from .worker import RideProducer


def produce_rides(request):
    """
        Creates rides as Kafka topics
    """
    # Create 5 rides ? maybe
    RideProducer()
    return HttpResponse('Success', status=200)


def book_ride(request):
    return render(request, 'uber/ride_map.html')


def get_rides_nearby(request):
    latitude = float(request.GET['latitude'])
    longitude = float(request.GET['longitude'])
    pickup_time = datetime.datetime(2014, 1, 1, 3, 25, 7)
    rides = get_rides(0.02, 0.02, 10, latitude, longitude, pickup_time)
    print(rides)
    markers = serializers.serialize('json', rides)


    # print(data)

    return HttpResponse(markers, content_type='application/json')


# def consume_rides(request):
#     RideConsumer()
#     return HttpResponse('Success', status=200)


# def ride_list(request):
#     rides = Ride.objects.filter(ride_date__lte=timezone.now()).order_by('ride_date')
#     return render(request, 'uber/ride_list.html', {'rides': rides})
#
#
# def ride_detail(request,pk):
#     ride = get_object_or_404(Ride, pk=pk)
#     return render(request, 'uber/ride_detail.html')
