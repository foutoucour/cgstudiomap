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
    jQuery.each(geoloc, function (i, val) {
        var contentString = '<div id="content">' + i + '</div>';

        var infowindow = new google.maps.InfoWindow({
            content: contentString
        });

        var marker = new google.maps.Marker({
            position: {lat: val[0], lng: val[1]},
            map: map,
            title: i
        });
        //extend the bounds to include each marker's position
        bounds.extend(marker.position);
        marker.addListener('click', function () {
            infowindow.open(map, marker);
        });
        markers.push(marker);

    });

    var mc = new MarkerClusterer(map, markers);
    //now fit the map to the newly inclusive bounds
    map.fitBounds(bounds);
    map.setOptions({styles: snazzy_theme()});
}

