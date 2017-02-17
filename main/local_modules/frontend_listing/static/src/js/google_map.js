/**
 * Script to manage the map displayed to list companies
 * Created by foutoucour on 12/10/15.
 * The theme of the map is loaded from `snazzy_theme.py` file.

 * CUSTOMS infos windows ref : http://en.marnoto.com/2014/09/5-formas-de-personalizar-infowindow.html
 */

function initialize(geoloc) {
    //To center map on markers
    var bounds = new google.maps.LatLngBounds();

    var mapCanvas = document.getElementById('map');
	
	
    var mapOptions = {
		minZoom: 3,
		gestureHandling: 'greedy',

        mapTypeId: google.maps.MapTypeId.ROADMAP,
        mapTypeControl: false,
        zoomControl: true,
        zoomControlOptions: {
            position: google.maps.ControlPosition.LEFT_CENTER
        },
        scaleControl: true,
        streetViewControl: true,
        streetViewControlOptions: {
            position: google.maps.ControlPosition.LEFT_CENTER
        }
    };
    var map = new google.maps.Map(mapCanvas, mapOptions);
    var markers = [];
    var icon = '/frontend_listing/static/src/marker.svg';
    var iconStudio = '/frontend_listing/static/src/marker-studio.svg';


    //INFOWINDOWS
    var infowindow = new google.maps.InfoWindow({
        //content: contentString,
        width: 250,
        maxWidth: 300
    });



    jQuery.each(geoloc, function (i, val) {
        var contentString = '<div id="content">' + val[2] + '</div>';

        var marker = new google.maps.Marker({
            position: {lat: val[0], lng: val[1]},
            map: map,
            icon: iconStudio,
            title: i
        });
        
        //extend the bounds to include each marker's position
        bounds.extend(marker.position);
        markers.push(marker);

        google.maps.event.addListener(marker, 'click', function () {
            infowindow.setContent(contentString);
            infowindow.open(map, marker);
        });

    });

    var clusterStyles = [
        {
            textColor: '#f1f1f3',
            url: icon,
            textSize: 18,
            height: 48,
            width: 48
        }
    ];

    var mcOptions = {
        gridSize: 50,
        styles: clusterStyles,
        maxZoom: 15
    };

    var mc = new MarkerClusterer(map, markers, mcOptions);
    //now fit the map to the newly inclusive bounds
    map.fitBounds(bounds);
    map.setOptions({styles: snazzy_theme()});
	
	
}

function getLocation() {
	// Try HTML5 geolocation.
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(function (position) {
			var pos = {
				lat: position.coords.latitude,
				lng: position.coords.longitude
			};
			infoWindow.setPosition(pos);
			infoWindow.setContent('Find around you.');
			map.setCenter(pos);
		}, function () {
			handleLocationError(true, infoWindow, map.getCenter());
		});
	}
	else {
		// Browser doesn't support Geolocation
		handleLocationError(false, infoWindow, map.getCenter());
	}
}


function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                          'Error: The Geolocation service failed.' :
                          'Error: Your browser doesn\'t support geolocation.');
}


google.maps.event.addDomListener(window, 'load', initialize);