function getPersonPopupContent(person) {
    var lat = person.geometry.coordinates[0];
    var lon = person.geometry.coordinates[1];
    var name = person.properties.name;
    var username = person.properties.username;
    var location_description = person.properties.location_description;
    var photo = person.properties.photo;
    var iso_code = person.properties.iso_code;
    var html =  '<ul class="detailsList">' + 
        '<li>' + 
        '<img src="' + photo + '" alt="' + name + '" class="main">' + 
        '<h3><a href="/' + username + '/">' + name + '</a></h3>' + 
        '<p class="meta"><a href="/' + iso_code + '/" class="nobg">' + 
        '<img src="' + STATIC_URL + 'djangopeople/img/flags/' + iso_code + '.gif"></a> ' + 
        location_description + '</p>' + 
        '<p class="meta"><a href="#" onclick="zoomOn(' + lat + ', ' + lon + '); return false;">Zoom to point</a></p>' +
        '</li>';
    return html;
}

function zoomOn(lat, lon) {
    MAP.setCenter(new L.LatLng(lat, lon));
    MAP.setZoom(12);
}

function greenIconImage() {
    var greenIcon = L.icon({
        iconUrl: STATIC_URL + 'djangopeople/img/green-bubble.png',
        shadowUrl: STATIC_URL + 'djangopeople/img/green-bubble-shadow.png',
        iconSize:     [32, 32], // size of the icon
        shadowSize:   [32, 32], // size of the shadow
        iconAnchor:   [16, 32], // point of the icon which will correspond to marker's location
        shadowAnchor: [10, 32],  // the same for the shadow
        popupAnchor:  [0, -32] // point from which the popup should open relative to the iconAnchor
    });
    return greenIcon;
}

L.TileLayer.ClusteredGeoJSONTile = L.TileLayer.extend({

    initClusterMarker: function (map) {
        var polygonOptions = {
            fillColor: "#ab5603",
            color: "#ab5603",
        }
        if (this.clusterMarker) {
            map.removeLayer(this.clusterMarker);
        }
        this.clusterMarker = new L.MarkerClusterGroup({
            "polygonOptions": polygonOptions
        });
    },

    initTmpLayer: function (e) {
        // Goal: add markers to cluster in one shot
        this.tmpLayer = new L.GeoJSON(null, {
            pointToLayer: function (feature, latlng) {
                var marker = new L.Marker(latlng, {
                    icon: greenIconImage(),
                });
                var info = getPersonPopupContent(feature);
                marker.bindPopup(info)
                return marker;
            }
        });
    },

    commitTmpLayer: function (e) {
        this.clusterMarker.addLayer(this.tmpLayer);
        if(!this._map.hasLayer(this.clusterMarker)) {
            // Add cluster layer to map after computing clusters, if needed
            // Cluster computing is always slower when ClusterLayer is
            // already displayed on map
            this._map.addLayer(this.clusterMarker)
        }
    },

    onAdd: function (map) {
        this._map = map;
        var self = this;
        map.on('zoomstart', function (e) {
            // Delete the cluster to prevent from having several times
            // the same people
            self.initClusterMarker(map);
        });
        this.on({
            'loading': this.initTmpLayer,
            'load': this.commitTmpLayer
        });
        L.TileLayer.prototype.onAdd.call(this, map);
    },

    _addTile: function (tilePoint, container) {
        L.TileLayer.prototype._addTile.call(this, tilePoint, container)

        var z = this._getZoomForUrl(),
            x = tilePoint.x,
            y = tilePoint.y;

        var dataUrl = L.Util.template(this.options.dataUrl, {
            s: this._getSubdomain(tilePoint),
            z: z,
            x: x,
            y: y
        });
        var self = this;
        $.getJSON(dataUrl, function (data) {
            DATA = data;
            self.tmpLayer.addData(data);
        });
    }

});