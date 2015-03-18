/**
 * Created by mark on 04/02/15.
 */

var map;

function main() {

    // Create basic map (OSM)
    map = L.map('map').setView([53.33, -6.27], 12);

    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
    }).addTo(map);

    // Add Lat/Lon popup
    map.on('click', onMapClick);

    // Add marker ...
    var marker = L.marker([53.33, -6.27]).addTo(map);
    // ... and bind it to a popup
    marker.bindPopup("<b>Hello world!</b><br>I am a popup in the initial centre of the map.").openPopup();

    // Add 'stand-alone' popup
//    var popup = L.popup()
//        .setLatLng([53.25, -6.2])
//        .setContent("I am a standalone popup.")
//        .openOn(map);

    // Catch current location and deal with errors if necessary
    map.locate({setView: true, maxZoom: 16});
    map.on('locationfound', onLocationFound);
    map.on('locationerror', onLocationError);

    // Add GeoJSON layer - Gaeltacht example
    L.geoJson(myGeoJson).addTo(map);
}


function onMapClick(e) {

    // Function to drive Lat/Lon popup
    var popup = L.popup();

    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(map);
}

function onLocationFound(e) {

    // React to location found event

    var radius = e.accuracy / 2;

    L.marker(e.latlng).addTo(map)
        .bindPopup("You are within " + radius + " meters from this point").openPopup();

    L.circle(e.latlng, radius).addTo(map);
}


function onLocationError(e) {

    // React to location error event

    alert(e.message);
}

