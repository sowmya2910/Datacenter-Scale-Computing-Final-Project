from django.db import models
from rest_framework import serializers
from .models import Ride


class RideSerializer(serializers.ModelSerializer):
    MESSAGE_TYPE = 'ride'
    VERSION = 1
    KEY_FIELD = 'id'

    class Meta:
        model = Ride
        fields = ['id']

    @classmethod
    def lookup_instance(cls, id, **kwargs):
        try:
            return Ride.objects.get(id=id)
        except models.Ride.DoesNotExist:
            pass


# class RideFindSerializer(serializers.ModelSerializer):
#     MESSAGE_TYPE = 'ride'
#     VERSION = 1
#     KEY_FIELD = 'id'
#
#     class Meta:
#         model = Ride
#         fields = ['id']
#
#     @classmethod
#     def lookup_instance(cls, id, **kwargs):
#         try:
#             return Ride.objects.get(id=id)
#         except models.Ride.DoesNotExist:
#             pass
