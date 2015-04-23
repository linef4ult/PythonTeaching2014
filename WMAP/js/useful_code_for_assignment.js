/**
 * Created by mark on 23/04/15.
 */

/*
* This file contains some useful functions to help in your assignment. The distance and bearing code is taken from the
* MovableType Scripts website (http://www.movable-type.co.uk/scripts/latlong.html)
*
* The rotate canvas function should be used in conjunction with the assignment.css file and uparrow_white_30.png image.
*
* To include a rotating image in your page, add the following div to the html page:
*
* <div id="dirArrow">
*    <canvas id="arrowCanvas" , width="30" , height="30">
*        Your browser does not support the HTML5 canvas tag.
*    </canvas>
* </div>
*
* */


function distance(lat1, lon1, lat2, lon2) {
    // This uses the ‘haversine’ formula to calculate the great-circle distance between two points – that is, the shortest
    // distance over the earth’s surface – giving an ‘as-the-crow-flies’ distance between the points (ignoring any hills
    // they fly over, of course!).
    //
    // Haversine formula: 	a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
    // c = 2 ⋅ atan2( √a, √(1−a) )
    // d = R ⋅ c
    // where 	φ is latitude, λ is longitude, R is earth’s radius (mean radius = 6,371km);
    // note that angles need to be in radians to pass to trig functions!

    var R = 6371000; // metres
    var φ1 = toRadians(lat1);
    var φ2 = toRadians(lat2);
    var Δφ = toRadians(lat2 - lat1);
    var Δλ = toRadians(lon2 - lon1);

    var a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
        Math.cos(φ1) * Math.cos(φ2) *
        Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return (d = R * c) / 1000;

}

function bearing(lat1, lon1, lat2, lon2) {
    // In general, your current heading will vary as you follow a great circle path (orthodrome); the final heading will
    // differ from the initial heading by varying degrees according to distance and latitude (if you were to go from say
    // 35°N,45°E (≈ Baghdad) to 35°N,135°E (≈ Osaka), you would start on a heading of 60° and end up on a heading of 120°!).
    //
    // This formula is for the initial bearing (sometimes referred to as forward azimuth) which if followed in a straight
    // line along a great-circle arc will take you from the start point to the end point:1
    // Formula: 	θ = atan2( sin Δλ ⋅ cos φ2 , cos φ1 ⋅ sin φ2 − sin φ1 ⋅ cos φ2 ⋅ cos Δλ )
    // JavaScript: (all angles in radians)

    var φ1 = toRadians(lat1);
    var λ1 = toRadians(lon1);
    var φ2 = toRadians(lat2);
    var λ2 = toRadians(lon2);

    var y = Math.sin(λ2 - λ1) * Math.cos(φ2);
    var x = Math.cos(φ1) * Math.sin(φ2) -
        Math.sin(φ1) * Math.cos(φ2) * Math.cos(λ2 - λ1);
    var brng = toDegrees(Math.atan2(y, x));

    if (brng < 0) {
        brng = (brng + 360) % 360;
    }

    return brng;


    // Since atan2 returns values in the range -π ... +π (that is, -180° ... +180°), to normalise the result to a
    // compass bearing (in the range 0° ... 360°, with −ve values transformed into the range 180° ... 360°), convert to
    // degrees and then use (θ+360) % 360, where % is (floating point) modulo.
    //
    // For final bearing, simply take the initial bearing from the end point to the start point and reverse it
    // (using θ = (θ+180) % 360).
}

// Converts from degrees to radians.
function toRadians(degrees) {
    return degrees * Math.PI / 180;
};

// Converts from radians to degrees.
function toDegrees(radians) {
    return radians * 180 / Math.PI;
};

function rotateCanvas(angle) {
    angle = toRadians(angle);

    var canvas = document.getElementById('arrowCanvas');
    var context = canvas.getContext('2d');

    context.clearRect ( 0 , 0 , canvas.width, canvas.height );

    var img1 = new Image();
    img1.src = "../images/uparrow_white_30.png";
    var imgWidth = img1.width;
    var imgHeight = img1.height;

    // translate context to center of canvas
    xpos = canvas.width / 2;
    ypos = canvas.height / 2;

    context.save();
    context.translate(xpos, ypos);
    context.rotate(angle);
    context.translate(-xpos, -ypos);
    context.drawImage(img1, xpos - imgWidth / 2, ypos - imgHeight / 2);
    context.restore();
}