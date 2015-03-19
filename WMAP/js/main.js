var map;
//var baseMaps = {};
//var overlayMaps = {};

var style = {
    "clickable": true,
    "color": "#ff0000",
    "fillColor": "#0000ff",
    "weight": 1.0,
    "opacity": 0.3,
    "fillOpacity": 0.2
};
//var hoverStyle = {
//	"fillOpacity": 0.5
//};

//var hexColours = [0xF1EEF6, 0xBDC9E1, 0x74A9CF, 0x2B8CBE, 0x045A8D];
//var decColours = [[241, 238, 246], [189, 201, 225], [116, 169, 207], [43, 140, 190], [4, 90, 141]];

var info = L.control({position: 'bottomleft'});

function main() {
    // Set up shortcuts for common tile providers
    var baseLayers = ['OpenCycleMap', 'OpenStreetMap.Mapnik', 'Thunderforest.Transport', 'Stamen.Watercolor',
        'Esri.WorldStreetMap'];

    //var overlays = ['OpenWeatherMap.Clouds'];

    // Initialize the map and set its view to our chosen geographical coordinates and a zoom level
    //By default all mouse and touch interactions on the map are enabled, and it has zoom and attribution controls.
    map = L.map('map', {zoomControl: false});
    var layerControl = L.control.layers.provided(baseLayers).addTo(map);
    map.fitBounds([[55.44, -10.88], [51.41, -5.88]]);

    // Settings for Info control
    info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
        this.update();
        return this._div;
    };
    // method that we will use to update the control based on feature properties passed
    info.update = function (props) {
        this._div.innerHTML = (props ? '<b>' + props.provname + '</b>' : '');
    };
    info.addTo(map);

    // When we click the map do something...
    map.on('click', onMapClick);
    map.on('overlayadd', onOverlayClick);

    // Script to do server-side processing, note full path including '?'
    var googleScript = 'cgi-bin/fromGoogleApi.py?';
    var wfsScript = 'cgi-bin/wfsProxy.py?';

    //
    // Add the layers
    //

    // Any WFS layers from our from Geoserver. Make an array of these
    var geoserverWorkspace = 'dit-wmap';
    var corsUrl = 'http://83.212.126.59:8080/geoserver/'+geoserverWorkspace+'/ows';
    var wfsLayers = ['Provinces', 'Counties', 'Cities_Towns'];

    for (i in wfsLayers) {
        var geoArgs = {
            'service': 'WFS',
            'request': 'GetFeature',
            'typeName': geoserverWorkspace + ':' + wfsLayers[i],
            'outputFormat': 'json',
            'srsName': 'epsg:4326'
        };
        var result = geoJsonCORS(corsUrl, geoArgs);
        layerControl.addOverlay(result, geoArgs['typeName']);
    }
    // Layers from Google Places
    var geoArgs = {
        'baseurl': 'https://maps.googleapis.com/maps/api/place/radarsearch/json',
        'location': '53.37,-6.28', 'key': 'AIzaSyCHTNoBNuVAPd0m07_s-4LK7KpgM-4uI88',
        'types': 'establishment', 'radius': '20000',
        'sensor': 'false'
    };
    placesLyr = geoJsonFromScript(googleScript, geoArgs);
    layerControl.addOverlay(placesLyr, "Google Places API");

    // Layer from Google Places (clustered)
    clusterLyr = showCluster(googleScript, geoArgs);
    layerControl.addOverlay(clusterLyr, "Google Places API (clustered)");

    // Array of GPX files
    gpxFiles = ["gpxfiles/20081123.gpx", "gpxfiles/20090305.gpx", "gpxfiles/20090417.gpx"];
    for (gpx in gpxFiles) {
        var track = new L.GPX(gpxFiles[gpx], {
            async: true, color: 'red', clickable: true
        });
        layerControl.addOverlay(track, gpxFiles[gpx]);
    }

    // 'cso:prgeom' - WMS from Geoserver
    layerControl.addOverlay(wmsLayer(geoArgs, "http://83.212.126.59:8080/geoserver/", 'dit-wmap', 'Counties'), "WMS Test (Counties)");

    //addGeoJson(geoArgs);
    //layerControl.addOverlay(addGeoJson(geoArgs), "std way");


    /*

     http://mf2.dit.ie/cgi-bin/fromGoogleApi.py?baseurl=https://maps.googleapis.com/maps/api/place/nearbysearch/json&location=53,-6&key=AIzaSyCHTNoBNuVAPd0m07_s-4LK7KpgM-4uI88&radius=20000&sensor=false

     */

    //layerControl = L.control.layers(null, overlayMaps).addTo(map);
    //var overlayMaps = {
    //	"Counties (WMS)": wmsLayer("http://mf2.dit.ie:8080/geoserver/", 'cso', 'prgeom'),
    //	"Counties (JSON - tile)": geoJsonLayer(geoArgs, "http://mf2.dit.ie:8080/geoserver/", 'cso', 'prgeom'),
    //	"Counties (JSON - std)": addGeoJson(geoArgs),
    //};

}

// Called when we click anywhere on the map
function onMapClick(e) {
    var popup = L.popup();
    // Create a popup with Lat/Lon
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(map);
}

// Render a WMS layer
function wmsLayer(geoArgs, serverbaseUrl, wrkSpace, lyrName) {
    var wmsLayer = L.tileLayer.wms(serverbaseUrl + wrkSpace + "/wms", {
        layers: wrkSpace + ':' + lyrName,
        format: 'image/png',
        transparent: true
    });

    return wmsLayer;
}

// Add GeoJSON layer using L.geoJson - the 'standard' way
function addGeoJson(geoArgs) {
    var fullUrl = 'cgi-bin/wfsProxy.py?';
    var qs = '';
    for (var k in geoArgs) {
        qs += k + '=' + geoArgs[k] + '&';
    }
    fullUrl = fullUrl + qs;

    thisLayer = L.geoJson(fullUrl,
        {
            style: style,
            onEachFeature: popUp,
        }).addTo(map);

    //return thisLayer;
}

// Render a GeoJSON layer using L.TileLayer.GeoJSON
function geoJsonLayer(geoArgs) {
    var fullUrl = 'cgi-bin/wfsProxy.py?';
    var qs = '';
    for (var k in geoArgs) {
        qs += k + '=' + geoArgs[k] + '&';
    }
    fullUrl = fullUrl + qs;

    var geojsonTileLayer = new L.TileLayer.GeoJSON(fullUrl, {
            clipTiles: true,
            unique: function (feature) {
                return feature.id;
            }
        }, {
            style: style,
            onEachFeature: popUp
        }
    );

    return geojsonTileLayer;
}

// Try leaflet.ajax.min.js plugin
// Try rendering GeoJSON from cgi proxy
function geoJsonCgi(geoArgs) {
    var fullUrl = 'cgi-bin/wfsProxy.py?';
    var qs = '';
    for (var k in geoArgs) {
        qs += k + '=' + geoArgs[k] + '&';
    }
    fullUrl = fullUrl + qs;

    var geoJsonLayer = L.geoJson.ajax(fullUrl,
        {
            style: style,
            onEachFeature: onEachFeature
        }
    );

    return geoJsonLayer;
}

function geoJsonCORS(url, args) {
    /*
     * Get GeoJSON from a CORS-enabled server. We need: url:port/path -- 'url' in this example
     * and a list of key:value arguments which come in as an associative array (object) and are sent as
     * key1=value1&key2=value2& ...
     */

    // 'fullUrl is the ajax query string comprising URL and key/value pairs. This is sent via AJAX.'
    var fullUrl = url + '?';

    var queryString = '';
    for (var k in args) {
        queryString += k + '=' + args[k] + '&';
    }

    fullUrl = fullUrl + queryString;

    // Make AJAX request and deal with response on a per-feature basis. AJAX needs to request from a CORS-enabled
    // server to work. Uses plugin from https://github.com/calvinmetcalf/leaflet-ajax.
    var geoJsonLayer = L.geoJson.ajax(fullUrl,
        {
            style: style,
            //onEachFeature: onEachFeature,
            onEachFeature: popUp
        }
    );

    // The results of the ajax request in geoJson format
    return geoJsonLayer;

}

// Show stuff from Google API
function fromGoogle(geoArgs) {
    var fullUrl = 'cgi-bin/fromGoogleApi.py?';
    var qs = '';
    for (var k in geoArgs) {
        qs += k + '=' + geoArgs[k] + '&';
    }
    fullUrl = fullUrl + qs;

    var geoJsonLayer = L.geoJson.ajax(fullUrl,
        {
            style: function (feature) {
                return L.icon({iconUrl: feature.properties.icon});
            },
            onEachFeature: popUp
        }
    );

    return geoJsonLayer;
}

// Generalised function to get geoJSON from any API - serverScript does the actual processing
function geoJsonFromScript(serverScript, geoArgs) {
    var qs = '';
    for (var k in geoArgs) {
        qs += k + '=' + geoArgs[k] + '&';
    }
    var fullUrl = serverScript + qs;

    var geoJsonLayer = L.geoJson.ajax(fullUrl,
        {
            style: style,
            onEachFeature: popUp
        }
    );

    return geoJsonLayer;
}

// Clustered points
function showCluster(serverScript, geoArgs) {
    var qs = '';
    for (var k in geoArgs) {
        qs += k + '=' + geoArgs[k] + '&';
    }
    var fullUrl = serverScript + qs;

    var markers = L.markerClusterGroup();

    var geoJsonLayer = L.geoJson.ajax(fullUrl,
        {
            onEachFeature: function (feature) {
                var out = [];
                for (key in feature.properties) {
                    out.push(key + ": " + feature.properties[key]);
                }
                if (feature.properties.icon) {
                    myIcon = L.icon({
                        iconUrl: feature.properties.icon,
                        iconSize: [24, 24],
                        className: "myIcon"
                    });
                } else {
                    myIcon = new L.Icon.Default;
                }
                var marker = L.marker(
                    L.latLng(feature.geometry.coordinates[1], feature.geometry.coordinates[0]),
                    {
                        icon: myIcon
                    }
                );
                marker.bindPopup(out.join("<br />"));
                markers.addLayer(marker);
            }
        }
    );

    return markers;
}

// Create popup for each GeoJSON feature
function popUp(feature, layer) {
    var out = [];
    if (feature.properties) {
        for (key in feature.properties) {
            out.push(key + ": " + feature.properties[key]);
        }
        layer.bindPopup(out.join("<br />"));
    }
}

function onOverlayClick(e) {
    map.fitBounds(e.layer.getBounds());
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
}

function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera) {
        layer.bringToFront();
    }

    info.update(layer.feature.properties);
}

function resetHighlight(e) {
    // TODO needs work - since change to WFS layers list, mouseout doesn't reset style
    //e.layer.resetStyle(e.target);
    e.resetStyle(style);
    info.update();
}

function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
}


/*
 ICON -- return L.icon({iconUrl: feature.icon, iconSize: [38, 95]}) else return L.icon.default

 L.icon({
 iconUrl: 'my-icon.png',
 iconRetinaUrl: 'my-icon@2x.png',
 iconSize: [38, 95],
 iconAnchor: [22, 94],
 popupAnchor: [-3, -76],
 shadowUrl: 'my-icon-shadow.png',
 shadowRetinaUrl: 'my-icon-shadow@2x.png',
 shadowSize: [68, 95],
 shadowAnchor: [22, 94]
 })

 function getColor(d) {
 return d > 1000 ? '#800026' :
 d > 500  ? '#BD0026' :
 d > 200  ? '#E31A1C' :
 d > 100  ? '#FC4E2A' :
 d > 50   ? '#FD8D3C' :
 d > 20   ? '#FEB24C' :
 d > 10   ? '#FED976' :
 '#FFEDA0';
 }

 function style(feature) {
 return {
 fillColor: getColor(feature.properties.density),
 weight: 2,
 opacity: 1,
 color: 'white',
 dashArray: '3',
 fillOpacity: 0.7
 };
 }

 function highlightFeature(e) {
 var layer = e.target;

 layer.setStyle({
 weight: 5,
 color: '#666',
 dashArray: '',
 fillOpacity: 0.7
 });

 if (!L.Browser.ie && !L.Browser.opera) {
 layer.bringToFront();
 }

 info.update(layer.feature.properties);
 }

 function resetHighlight(e) {
 geojson.resetStyle(e.target);
 info.update();
 }

 function zoomToFeature(e) {
 map.fitBounds(e.target.getBounds());
 }

 function onEachFeature(feature, layer) {
 layer.on({
 mouseover: highlightFeature,
 mouseout: resetHighlight,
 click: zoomToFeature
 });
 }

 var info = L.control();

 info.onAdd = function (map) {
 this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
 this.update();
 return this._div;
 };

 // method that we will use to update the control based on feature properties passed
 info.update = function (props) {
 this._div.innerHTML = '<h4>US Population Density</h4>' +  (props ?
 '<b>' + props.name + '</b><br />' + props.density + ' people / mi<sup>2</sup>'
 : 'Hover over a state');
 };

 info.addTo(map);

 var legend = L.control({position: 'bottomright'});

 legend.onAdd = function (map) {

 var div = L.DomUtil.create('div', 'info legend'),
 grades = [0, 10, 20, 50, 100, 200, 500, 1000],
 labels = [];

 // loop through our density intervals and generate a label with a colored square for each interval
 for (var i = 0; i < grades.length; i++) {
 div.innerHTML +=
 '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
 grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
 }

 return div;
 };

 legend.addTo(map);

 //CSS stuff
 .info {
 padding: 6px 8px;
 font: 14px/16px Arial, Helvetica, sans-serif;
 background: white;
 background: rgba(255,255,255,0.8);
 box-shadow: 0 0 15px rgba(0,0,0,0.2);
 border-radius: 5px;
 }
 .info h4 {
 margin: 0 0 5px;
 color: #777;
 }
 .legend {
 line-height: 18px;
 color: #555;
 }
 .legend i {
 width: 18px;
 height: 18px;
 float: left;
 margin-right: 8px;
 opacity: 0.7;
 }


 */
