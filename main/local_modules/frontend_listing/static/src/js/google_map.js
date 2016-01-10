/**
 * Script to manage the map displayed to list companies
 * Created by foutoucour on 12/10/15.
 * The theme of the map is loaded from `snazzy_theme.py` file.
 */

function initialize(geoloc) {
    //To center map on markers
    var bounds = new google.maps.LatLngBounds();

    var mapCanvas = document.getElementById('map');
    var mapOptions = {
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(mapCanvas, mapOptions);

    var markers = [];
    var icon = '/frontend_listing/static/src/marker.svg';
    var iconStudio = '/frontend_listing/static/src/marker-studio.svg';
    jQuery.each(geoloc, function (i, val) {
        var contentString = '<div id="content">' + val[2] + '</div>';
        var infowindow = new google.maps.InfoWindow({
            content: contentString
        });

        var marker = new google.maps.Marker({
            position: {lat: val[0], lng: val[1]},
            map: map,
            icon: iconStudio,
            title: i
        });
        //extend the bounds to include each marker's position
        bounds.extend(marker.position);
        marker.addListener('click', function () {
            infowindow.open(map, marker);
        });
        markers.push(marker);

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

