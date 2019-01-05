from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    # path('', views.ride_list, name='ride_list'),
    # path('post/<int:pk>/', views.ride_detail, name='ride_detail'),
    path('ride/produce', views.produce_rides, name='produce_ride'),
    path('ride/search', views.book_ride, name='book_ride'),
    path('ride/get', views.get_rides_nearby, name='get_ride'),
    # path('ride/consume', views.consume_rides, name="consume_ride"),
    # url(r'', views.default_map, name="ride_map"),
]
