window.onload = function() {    
    var personLatLng =  new google.maps.LatLng(person_latitude, person_longitude);

    function ShrinkControl(button) {
        button.innerHTML = 'Shrink map';
        button.style.color = "black";
        button.style.backgroundColor = "white";
        button.style.font = "12px Arial";
        button.style.border = "1px solid black";
        button.style.padding = "2px";
        button.style.marginBottom = "3px";
        button.style.textAlign = "center";
        button.style.width = "6em";
        button.style.cursor = "pointer";

        google.maps.event.addDomListener(button, "click", function() {
            $('#gmap').css({'cursor': 'pointer'}).attr(
                'title', 'Activate larger map'
            );
            gmap.controls[google.maps.ControlPosition.BOTTOM_LEFT].clear();
            //hideNearbyPeople(gmap);
            $('#gmap').animate({
                height: '7em',
                opacity: 0.6
            }, 500, 'swing', function() {
                google.maps.event.trigger(gmap, 'resize');
                gmap.setCenter(personLatLng);
                gmap.setOptions({draggable: false});
                $('#gmap').click(onMapClicked);
            });
        });
    }

    var myOptions = {
        zoom: 12,
        center: personLatLng,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        draggable: false,
        disableDefaultUI: true
    };
    var gmap = new google.maps.Map(document.getElementById('gmap'), myOptions);

    var shrinkButtonDiv = document.createElement('div');
    var shrinkButton = new ShrinkControl(shrinkButtonDiv);
    shrinkButtonDiv.index = 1;


    /* Map enlarges and becomes active when you click on it */
    $('#gmap').css({'cursor': 'pointer', 'opacity': 0.6}).attr(
            'title', 'Activate larger map'
            );
    function onMapClicked() {
        $('#gmap').css({'cursor': ''}).attr('title', '');
        $('#gmap').animate({
            height: '25em',
            opacity: 1.0
        }, 500, 'swing', function() {
            google.maps.event.trigger(gmap, 'resize');
            gmap.panTo(personLatLng);
            gmap.setOptions({draggable: true});
            //showNearbyPeople(gmap);
            // Unbind event so user can actually interact with map
            $('#gmap').unbind('click', onMapClicked);
        });
        gmap.controls[google.maps.ControlPosition.BOTTOM_LEFT].push(shrinkButtonDiv);
    }
    $('#gmap').click(onMapClicked);

    var marker = new google.maps.Marker({
        position: personLatLng,
        map: gmap
    });
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

    if ($('#uploadNewPhoto').length && $('div.header img.main').length) {
        var href = $('a#uploadNewPhoto').attr('href');
        $('#uploadNewPhoto').remove();
        var upload = $('<a href="' + href + '">(replace)</a>').appendTo(
            document.body
            );
        var img = $('div.header img.main');
        upload.css({
            'font-size': '10px',
            'text-decoration': 'none',
            'color': 'white',
            'padding': '0px 2px 0px 2px',
            'background-color': 'black',
            'position': 'absolute',
            'top': img.offset().top + img.height() - upload.height() - 1,
            'left': img.offset().left + 4,
            'visibility': 'hidden'
        });
        img.mouseover(function() {
            upload.css('visibility', 'visible');
        });
        upload.mouseover(function() {
            upload.css('visibility', 'visible');
        });
        img.mouseout(function() {
            upload.css('visibility', 'hidden');
        });
    }
    /*    
    // Hide changeloc link too
    if ($('a.changeloc').length) {
    $('a.changeloc').css('visibility', 'hidden');
    $('a.changeloc').parent().mouseover(function() {
    $('a.changeloc').css('visibility', 'visible');
    });
    $('a.changeloc').parent().mouseout(function() {
    $('a.changeloc').css('visibility', 'hidden');
    });
    $('a.changeloc').mouseover(function() {
    $('a.changeloc').css('visibility', 'visible');
    });
    }

    // And tags edit
    if ($('ul.tags li.edit').length) {
    var a = $('ul.tags li.edit a').css('text-decoration', 'none');
    a.css('visibility', 'hidden');
    a.parent().parent().mouseover(function() {
    a.css('visibility', 'visible');
    });
    a.parent().parent().mouseout(function() {
    a.css('visibility', 'hidden');
    });
    a.mouseover(function() {
    a.css('visibility', 'visible');
    });
    }

    // And the edit links in the h2s
    $('h2 a.edit').each(function() {
    var $this = $(this);
    $this.css('visibility', 'hidden');
    $this.parent().mouseover(function() {
    $this.css('visibility', 'visible');
    });
    $this.parent().mouseout(function() {
    $this.css('visibility', 'hidden');
    });
    $this.mouseover(function() {
    $this.css('visibility', 'visible');
    });
    });

    // And the edit bio link
    if ($('div.bio a.edit').length) {
    $div = $('div.bio');
    $a = $('div.bio a.edit');
    $a.css('visibility', 'hidden');
    $div.mouseover(function() {
    $a.css('visibility', 'visible');
    });
    $div.mouseout(function() {
    $a.css('visibility', 'hidden');
    });
    $a.mouseover(function() {
    $a.css('visibility', 'visible');
    });
    }
    */    
});
