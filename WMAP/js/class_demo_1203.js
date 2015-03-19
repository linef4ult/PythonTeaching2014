/**
 * Created by mark on 12/03/15.
 */

var map;

function main() {
    // create basic map
    map = L.map("map");
    map.setView([53.5, -8.5], 12);

    my_tiles = L.tileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 18
    });
    my_tiles.addTo(map);

    // add lat/lon popup
    map.on("click", onMapClick);
}

function onMapClick(e) {
    // put a lat/lon popup on the map
    var popup = L.popup();

    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at "+ e.latlng.toString())
        .openOn(map);

}