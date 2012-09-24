function shrinkMap (map, latlng) {
    // Center map
    map.panTo(latlng);

    var ShrinkMapControl = L.Control.extend({
        options: {
            position: 'bottomleft'
        },

        onAdd: function (map) {
            // create the control container with a particular class name
            var container = L.DomUtil.create('div', 'shrinkControl');
            container.innerHTML = 'Shrink map';
            L.DomEvent.addListener(container, 'click', this.onClick, this);

            return container;
        },

        onClick: function () {
            $('#map').css({'cursor': 'pointer'}).attr(
                'title', 'Activate larger map'
            );
            $('#map').animate({
                height: '7em',
                opacity: 0.6
            }, 500, 'swing', function() {
                map._onResize()
                $('#map').click(onMapClicked);
                shrinkControl.removeFrom(map);
            });

        }
    });
    var shrinkControl = new ShrinkMapControl();

    /* Map enlarges and becomes active when you click on it */
    $('#map').css({'cursor': 'pointer', 'opacity': 0.6}).attr(
            'title', 'Activate larger map'
            );
    function onMapClicked() {
        $('#map').css({'cursor': ''}).attr('title', '');
        $('#map').animate({
            height: '25em',
            opacity: 1.0
        }, 500, 'swing', function() {
            map._onResize()
            // showPeopleOnMap(peopleArray, map);

            // Unbind event so user can actually interact with map
            $('#map').unbind('click', onMapClicked);
            shrinkControl.addTo(map);
        });
    }
    $('#map').click(onMapClicked);


    // Marker for the current profile, not clickable
    var marker = new L.Marker(latlng, {
        icon: greenIconImage(),
    }).addTo(map);

    //gets an array of person map markers, used for hiding and showing them on
    //the map
    // var peopleArray = getPeopleArray(nearby_people);

};

jQuery(function($) {
    $('#editSkills').hide();
    $('ul.tags li.edit a').toggle(
        function() {
            $('#editSkills').show();
            return false;
        },
        function() {
            $('#editSkills').hide();
            return false;
        }
        );
});
