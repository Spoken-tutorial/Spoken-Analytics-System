// JS for Visitor Map Page

var layers; // Leaflet layers object

function onEachFeature(feature, layer) {
    if (feature.properties) {
        layer.bindPopup("<span>" + feature.properties.ip_address + "</span>");
    }
}

// Function is called automatically when map is initialized
function map_init(map, options) {

    visitor_map = map

    map.eachLayer(function(layer) {
        map.removeLayer(layer);
    });

    L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', { subdomains: ['mt0', 'mt1', 'mt2', 'mt3'] }).addTo(map);
    layers = L.geoJson(false, { onEachFeature: onEachFeature }).addTo(map);
    map.addControl(new L.Control.Fullscreen());
}


// Getting date between two timestamps
function getData() {
    var date = $('#date').val();
    var start_time = $('#start-time').val();
    var end_time = $('#end-time').val();
    from = moment(date + " " + start_time).format('YYYY-MM-DD HH:mm');
    to = moment(date + " " + end_time).format('YYYY-MM-DD HH:mm');

    $.ajax({
        type: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': window.CSRF_TOKEN,
            'Accept': 'application/json'
        },
        data: JSON.stringify({
            from: from,
            to: to,
        }),
        url: "/dashboard/visitor_map_data/",
        success: function(data) {

            // Parsing the data
            data = JSON.parse(data);

            // Clearing existing data from map
            layers.clearLayers();

            // Adding new data to map
            layers.addData(data);
        },
        error: function(err) {
            console.log("Error:" + err);
        }
    });
}

$(function() {
    getData();
});