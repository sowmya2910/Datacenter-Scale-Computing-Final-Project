var ride_found = false;
var rides = null;
var pickup_set = false;
var dropff_set = false;
var pickup_marker = {
    lat: null,
    lng: null
}

var dropoff_marker = {
    lat: null,
    lng: null
}

    // Initialize and add the map
    function initMap() {
      var map = new google.maps.Map(
          document.getElementById('map'),
          {zoom: 10,
          styles: [
                {elementType: 'geometry', stylers: [{color: '#242f3e'}]},
                {elementType: 'labels.text.stroke', stylers: [{color: '#242f3e'}]},
                {elementType: 'labels.text.fill', stylers: [{color: '#746855'}]},
                {
                  featureType: 'administrative.locality',
                  elementType: 'labels.text.fill',
                  stylers: [{color: '#d59563'}]
                },
                {
                  featureType: 'poi',
                  elementType: 'labels.text.fill',
                  stylers: [{color: '#d59563'}]
                },
                {
                  featureType: 'poi.park',
                  elementType: 'geometry',
                  stylers: [{color: '#263c3f'}]
                },
                {
                  featureType: 'poi.park',
                  elementType: 'labels.text.fill',
                  stylers: [{color: '#6b9a76'}]
                },
                {
                  featureType: 'road',
                  elementType: 'geometry',
                  stylers: [{color: '#38414e'}]
                },
                {
                  featureType: 'road',
                  elementType: 'geometry.stroke',
                  stylers: [{color: '#212a37'}]
                },
                {
                  featureType: 'road',
                  elementType: 'labels.text.fill',
                  stylers: [{color: '#9ca5b3'}]
                },
                {
                  featureType: 'road.highway',
                  elementType: 'geometry',
                  stylers: [{color: '#746855'}]
                },
                {
                  featureType: 'road.highway',
                  elementType: 'geometry.stroke',
                  stylers: [{color: '#1f2835'}]
                },
                {
                  featureType: 'road.highway',
                  elementType: 'labels.text.fill',
                  stylers: [{color: '#f3d19c'}]
                },
                {
                  featureType: 'transit',
                  elementType: 'geometry',
                  stylers: [{color: '#2f3948'}]
                },
                {
                  featureType: 'transit.station',
                  elementType: 'labels.text.fill',
                  stylers: [{color: '#d59563'}]
                },
                {
                  featureType: 'water',
                  elementType: 'geometry',
                  stylers: [{color: '#17263c'}]
                },
                {
                  featureType: 'water',
                  elementType: 'labels.text.fill',
                  stylers: [{color: '#515c6d'}]
                },
                {
                  featureType: 'water',
                  elementType: 'labels.text.stroke',
                  stylers: [{color: '#17263c'}]
                }
              ]});

       var pickup_marker = null;


       map.addListener('click', function(e) {
            placeMarker(e.latLng, map);
       });

      // The location of Uluru
      var uluru = {lat: 40.71139144897461, lng:-73.9468765258789};
      map.setCenter(uluru);
      if (ride_found) {
        setMarkers(rides, map);
      }
}
    function placeMarker(location, map) {
        if (pickup_set && dropff_set) {
            return;
        }

        var marker = new google.maps.Marker({
            position: location,
            map: map
        });

        if (!pickup_set) {
            map.panTo(location);
            pickup_marker = location;
            pickup_set = true;
        }
        else {
            dropff_set = true;
            dropoff_marker = location;
        }

        map.setZoom(13);
    }

    function setPickDropMarkers(map) {
        var pick_marker = new google.maps.Marker({
            position: pickup_marker,
            map: map,
            title: "source"
        });

        var drop_marker = new google.maps.Marker({
            position: dropoff_marker,
            map: map,
            title: "destination"
        });

        map.setCenter(pickup_marker)
        map.setZoom(11);
    }

    var setMarkers = function(rides, map) {
        setPickDropMarkers(map);
        var pickup_time = new Date("2014-01-01T03:25:07Z");

//        var pickup_location = {lat: rides.source.pickup_latitude, lng: rides.source.pickup_longitude};
        map.setCenter(pickup_marker);
        map.setZoom(13);

        var markers = rides;
        for (i = 0; i < markers.length; i++) {
            latitude = markers[i].fields.pickup_latitude
            longitude = markers[i].fields.pickup_longitude
            time = new Date(markers[i].fields.pickup_datetime)
            // time it takes for the cab to reach the source for pickup
            arrival = Math.abs(pickup_time.getMinutes() - time.getMinutes())
            var marker = new google.maps.Marker({
            position: new google.maps.LatLng(latitude, longitude),
            icon: {
                url: "https://cdn0.iconfinder.com/data/icons/car-with-sensor/100/Car_Location-512.png",
//                anchor: new google.maps.Point(30, 30.26),
                scaledSize: new google.maps.Size(50, 50),

            },
            map: map
          });
        }
    }

     $('#ride-search').click(function(){
         data_to_be_sent = {
            latitude: pickup_marker.lat,
            longitude: pickup_marker.lng
         }
         $.get('/ride/get', data_to_be_sent, function(data){
            ride_found = true;
            rides = data;
            initMap();
          });
    });
