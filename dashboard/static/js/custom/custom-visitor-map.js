// JS for Visitor Map Page

function onEachFeature(feature, layer) {
    if (feature.properties && feature.properties.popupContent) {
        layer.bindPopup(feature.properties.popupContent);
    }
}

function map_init(map, options) {

    map.eachLayer(function(layer) {
        map.removeLayer(layer);
    });

    L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', { subdomains: ['mt0', 'mt1', 'mt2', 'mt3'] }).addTo(map);
    L.geoJson(collection, { onEachFeature: onEachFeature }).addTo(map);
    map.addControl(new L.Control.Fullscreen());
}