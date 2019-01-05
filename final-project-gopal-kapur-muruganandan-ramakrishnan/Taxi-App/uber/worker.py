import datetime
from .models import Ride
from .serializer import RideSerializer
from logpipe import Producer, Consumer


def RideProducer():
    """
        Create a ride
    """

    ride_obj = Ride.objects.create(vendorid=18,
                                   pickup_datetime=datetime.datetime.now(),
                                   dropoff_datetime=datetime.datetime.now() + datetime.timedelta(minutes=15),
                                   rate_code=1,
                                   pickup_longitude=-73.95162200927734,
                                   pickup_latitude=40.71432876586913,
                                   dropoff_longitude=-73.95046997070312,
                                   dropoff_latitude=40.71106338500977,
                                   passenger_count=2,
                                   trip_distance=2.4,
                                   fare_amount=10,
                                   tip_amount=1,
                                   total_amount=11,
                                   payment_type=1)

    producer = Producer('ride', RideSerializer)
    producer.send(ride_obj)


# def RideConsumer():
#     consumer = Consumer('ride', consumer_timeout_ms=1000)
#     consumer.register(RideSerializer)
#     consumer.run()
