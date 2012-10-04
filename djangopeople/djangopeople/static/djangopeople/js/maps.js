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

L.PeopleMarker = L.Marker.extend({

    initialize: function(person_id, latlng, options) {
        this.person_id = person_id;

        L.Marker.prototype.initialize.call(this, latlng, options);

        // Events
        this.on("click", this._onClick);
    },

    _onClick: function() {
        (function(self){
            $.ajax(self.person_id + "/popup/").done(function (html) {
                self.bindPopup(html);
                self.openPopup();
            });
        })(this)
    }

});

L.TileLayer.ClusteredGeoJSONTile = L.TileLayer.extend({

    initClusterMarker: function (map) {
        this._geojsonTilesToLoad = 0;
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
                var marker = new L.PeopleMarker(feature.id, latlng, {
                    icon: greenIconImage()
                });
                // var info = getPersonPopupContent(feature);
                // marker.bindPopup(" " + feature.id)
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
            'geojsonloadinit': this.initTmpLayer,
            'geojsonloadend': this.commitTmpLayer
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
        if(!this._geojsonTilesToLoad) {
            this.fire("geojsonloadinit")
        }
        // Register that this tile is not yet loaded
        this._geojsonTilesToLoad++;
        $.getJSON(dataUrl, function (data) {
            DATA = data;
            self.tmpLayer.addData(data);
            // Tile loaded
            self._geojsonTilesToLoad--;
            if(!self._geojsonTilesToLoad) {
                // No more tiles to load
                self.fire("geojsonloadend")
            }
        });
    }

});