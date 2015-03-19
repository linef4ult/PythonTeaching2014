/**
 * Created by mark on 05/03/15.
 */

// The 'real' work happens here.

// Create a 'map' variable. This will be global as we'll interact with it all over the place.
var map;
var baseMaps = {};
var overlayMaps = {};

function main() {
    // Called at the body 'onload' event. This is the entry point for your JavaScript

    // Set up shortcuts for common tile providers
    var baseLayers = ["OpenCycleMap", "OpenStreetMap.Mapnik", "Thunderforest.Transport", "Stamen.Watercolor",
        "Esri.WorldStreetMap"];
    // Initialize the map and set its view to our chosen geographical coordinates and a zoom level
    //By default all mouse and touch interactions on the map are enabled, and it has zoom and attribution controls.
    map = L.map("map", {zoomControl: false});
    var layerControl = L.control.layers.provided(baseLayers).addTo(map);
    map.fitBounds([[55.44, -10.88], [51.41, -5.88]]);
}