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
            $.ajax("/" + self.person_id + "/popup/").done(function (html) {
                self.bindPopup(html);
                self.openPopup();
            });
        })(this)
    }

});

L.ClusterMarker = L.Marker.extend({

    onAdd: function(map) {
        L.Marker.prototype.onAdd.call(this, map);

        this.on("click", this._onClick);
    },

    _onClick: function() {
        var current_zoom = this._map.getZoom();
        this._map.setView(this.getLatLng(), current_zoom + 1)
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

    initServerClustersLayer: function (map) {
        if (this.serverClusterLayer) {
            map.removeLayer(this.serverClusterLayer);
        }
        this.serverClusterLayer = new L.GeoJSON(null, {
            pointToLayer: function (feature, latlng) {
                var childCount = feature.properties.len
                var c = ' marker-cluster-';
                if (childCount < 10) {
                    c += 'small';
                } else if (childCount < 100) {
                    c += 'medium';
                } else {
                    c += 'large';
                }
                var marker = new L.ClusterMarker(latlng, {
                    icon: new L.DivIcon({ html: '<div><span>' + childCount + '</span></div>', className: 'marker-cluster' + c, iconSize: new L.Point(40, 40) })
                });
                return marker;
            }
        });
    },

    detachServerClusterLayer: function () {
        if (typeof this._map !== "undefined" && this._map.hasLayer(this.serverClusterLayer)) {
            this._map.removeLayer(this.serverClusterLayer)
        }
    },

    loadServerClusters: function () {
        this._map.addLayer(this.serverClusterLayer)
        var self = this;
        $.getJSON("/clusters/" + this._getZoomForUrl(), function (data) {
            DATA = data;
            self.serverClusterLayer.addData(data);
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
        this.zoomSwitchAt = 5
        map.on('zoomstart', function (e) {
            // Delete the clusters to prevent from having several times
            // the same people
            self.initClusterMarker(map);
            self.initServerClustersLayer(map);

        });
        map.on('zoomend', function (e) {
            if (self._getZoomForUrl() <= self.zoomSwitchAt) {
                self.loadServerClusters();
            }
        });
        this.on({
            'geojsonloadinit': this.initTmpLayer,
            'geojsonloadend': this.commitTmpLayer
        });
        L.TileLayer.prototype.onAdd.call(this, map);
    },

    _addJSONTile: function (tilePoint, container) {
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
    },

    _addTile: function (tilePoint, container) {
        L.TileLayer.prototype._addTile.call(this, tilePoint, container)
        if (this._getZoomForUrl() > this.zoomSwitchAt) {
            this._addJSONTile(tilePoint, container);
        }
    }

});