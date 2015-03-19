/**
 * Created by mark on 18/03/15.
 */

var map;

var style = {
    "clickable": true,
    "color": "#ff0000",
    "fillColor": "#0000ff",
    "weight": 1.0,
    "opacity": 0.3,
    "fillOpacity": 0.2
};

// A little 'info' widget on the bottom left of the map - see below
var info = L.control({position: 'bottomleft'});

function main() {
    // Set up shortcuts for common tile providers
    var baseLayers = ['OpenCycleMap', 'OpenStreetMap.Mapnik', 'Thunderforest.Transport', 'Stamen.Watercolor',
        'Esri.WorldStreetMap'];

    // Initialize the map and set its view to our chosen geographical coordinates and a zoom level
    //By default all mouse and touch interactions on the map are enabled, and it has zoom and attribution controls.
    map = L.map('map', {zoomControl: false});
    var layerControl = L.control.layers.provided(baseLayers).addTo(map);
    map.fitBounds([[55.44, -10.88], [51.41, -5.88]]);

    // Settings for Info control - see above
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

    //
    // Add the layers
    //

    // Any WFS layers from our from Geoserver. Make an array of these. Note that the server providing these must be
    // CORS-enabled
    var geoserverWorkspace = 'dit-wmap';
    var corsUrl = 'http://83.212.126.59:8080/geoserver/' + geoserverWorkspace + '/ows';
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

    // Array of GPX files
    gpxFiles = ["../gpxfiles/20081123.gpx", "../gpxfiles/20090305.gpx", "../gpxfiles/20090417.gpx"];
    for (gpx in gpxFiles) {
        var track = new L.GPX(gpxFiles[gpx], {
            async: true, color: 'red', clickable: true
        });
        layerControl.addOverlay(track, gpxFiles[gpx]);
    }

    // Any WMS layers from Geoserver. Note that this is more straightforward than dealing with WFS (mainly die to CORS
    // issues). There is one layer (Counties) in this example.
    layerControl.addOverlay(
        wmsLayer("http://83.212.126.59:8080/geoserver/", 'dit-wmap', 'Counties'), "WMS Test (Counties)"
    );
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

// Render geoJSON from a server using the WFS protocol. Note that AJAX is driving the request to the server. Note also
// that this approach is susceptible to CORS issues. The server needs to be configured to handle this.
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

// Render a WMS layer
function wmsLayer(serverbaseUrl, wrkSpace, lyrName) {
    var wmsLayer = L.tileLayer.wms(serverbaseUrl + wrkSpace + "/wms", {
        layers: wrkSpace + ':' + lyrName,
        format: 'image/png',
        transparent: true
    });

    return wmsLayer;
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
