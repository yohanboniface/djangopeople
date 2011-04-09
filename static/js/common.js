jQuery(function($) {
    $('div.nav a.login').click(function() {
        // Show inline login form
        $('div#hiddenLogin').show().css({
            position: 'absolute',
            top: $(this).offset().top + $(this).height() + 7,
            left: $(this).offset().left
        });
        $('#id_usernameH').focus();
        return false;
    });
});

function makeWindow(name, username, location, photo, iso_code, lat, lon) {
    var html =  '<ul class="detailsList">' + 
        '<li>' + 
        '<img src="' + photo + '" alt="' + name + '" class="main">' + 
        '<h3><a href="/' + username + '/">' + name + '</a></h3>' + 
        '<p class="meta"><a href="/' + iso_code + '/" class="nobg">' + 
        '<img src="/static/img/flags/' + iso_code + '.gif"></a> ' + 
        location + '</p>' + 
        '<p class="meta"><a href="#" onclick="zoomOn(' + lat + ', ' + lon + '); return false;">Zoom to point</a></p>' +
        '</li>';
    return html;
}

function zoomOn(lat, lon) {
    //gmap.closeInfoWindow();
    gmap.setCenter(new google.maps.LatLng(lat, lon), 12);
}

function hidePeopleOnMap(peopleArray) {
    if (peopleArray) {
        for (i in peopleArray) {
            peopleArray[i].setMap(null);
        }
    }
}

function showPeopleOnMap(peopleArray, map) {
    if (peopleArray) {
        for (i in peopleArray) {
            peopleArray[i].setMap(map);
        }
    }
}

function getPeopleArray(peopleList) {
    var peopleArray = [];
    $.each(peopleList, function() {
        var lat = this[0];
        var lon = this[1];
        var name = this[2];
        var username = this[3];
        var location_description = this[4];
        var photo = this[5];
        var iso_code = this[6];
        var point = new google.maps.LatLng(lat, lon);

        var marker = new google.maps.Marker({
            position: point
        });

        peopleArray.push(marker);

        var infoWindow = new google.maps.InfoWindow({
            content: makeWindow(
                         name, username, location_description, photo, iso_code, 
                         lat, lon
                         )
        });

        // Hook up the marker click event
        google.maps.event.addListener(marker, 'click', function() {
            infoWindow.open(gmap, marker);
        });
    });

    return peopleArray;
}

function getMarkerOpts() {
    var greenIcon = new google.maps.Icon(google.maps.DEFAULT_ICON);
    greenIcon.image = "/static/img/green-bubble.png";
    greenIcon.iconSize = new google.maps.Size(32,32);
    greenIcon.shadowSize = new google.maps.Size(56,32);
    greenIcon.iconAnchor = new google.maps.Point(16,32);
    greenIcon.infoWindowAnchor = new google.maps.Point(16,0); 
    markerOpts = { icon: greenIcon };
    return markerOpts;
}

