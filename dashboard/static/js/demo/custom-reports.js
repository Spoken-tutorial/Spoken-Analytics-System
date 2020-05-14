$("#tile-1 .nav-tabs a").click(function() {
    var position = $(this).parent().position();
    var width = $(this).parent().width();
    $("#tile-1 .slider").css({ "left": +position.left, "width": width });
});
var actWidth1 = $("#tile-1 .nav-tabs").find(".active").parent("li").width();
var actPosition1 = $("#tile-1 .nav-tabs .active").position();
$("#tile-1 .slider").css({ "left": +actPosition1.left, "width": actWidth1 });

$("#tile-2 .nav-tabs a").click(function() {
    var position = $(this).parent().position();
    var width = $(this).parent().width();
    $("#tile-2 .slider").css({ "left": +position.left, "width": width });
});
var actWidth2 = $("#tile-2 .nav-tabs").find(".active").parent("li").width();
var actPosition2 = $("#tile-2 .nav-tabs .active").position();
$("#tile-2 .slider").css({ "left": +actPosition2.left, "width": actWidth2 });


$(document).ready(function() {
    $.ajax({
        type: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': window.CSRF_TOKEN,
            'Accept': 'application/json'
        },
        url: "/dashboard/location_stats/",
        success: function(data) {

            console.log(data)

            // Parsing the data
            region_stats = JSON.parse(data.region_stats);
            city_stats = JSON.parse(data.city_stats);
            total_page_views = JSON.parse(data.total_page_views);
            foss_stats = JSON.parse(data.foss_stats);
            total_foss_page_views = JSON.parse(data.total_foss_page_views);

            console.log(foss_stats, total_foss_page_views);

            var region_table = $("#region-table tbody");
            var city_table = $("#city-table tbody");
            var foss_table = $("#foss-table tbody");
            var pages_table = $("#pages-table tbody");

            region_stats.forEach((key, value) => {
                region_table.append("<tr><td>" + key.fields.region + "</td><td><div class='progress progress-sm mb-2' style='margin-top: 0.7em;'><div class='progress-bar' role='progressbar' style='width: " + (key.fields.page_views / total_page_views).toFixed(2) * 100 + "%' aria-valuenow='44.3' aria-valuemin='0' aria-valuemax='100'></div></div></td><td>" + ((key.fields.page_views / total_page_views) * 100).toFixed(2) + "%</td></tr>");
            });

            city_stats.forEach((key, value) => {
                city_table.append("<tr><td>" + key.fields.city + "</td><td><div class='progress progress-sm mb-2' style='margin-top: 0.7em;'><div class='progress-bar' role='progressbar' style='width: " + (key.fields.page_views / total_page_views).toFixed(2) * 100 + "%' aria-valuenow='44.3' aria-valuemin='0' aria-valuemax='100'></div></div></td><td>" + ((key.fields.page_views / total_page_views) * 100).toFixed(2) + "%</td></tr>");
            });

            foss_stats.forEach((key, value) => {
                foss_table.append("<tr><td>" + key.foss_name + "</td><td><div class='progress progress-sm mb-2' style='margin-top: 0.7em;'><div class='progress-bar' role='progressbar' style='width: " + (key.page_views / total_foss_page_views).toFixed(2) * 100 + "%' aria-valuenow='44.3' aria-valuemin='0' aria-valuemax='100'></div></div></td><td>" + ((key.page_views / total_foss_page_views) * 100).toFixed(2) + "%</td></tr>");
            });
        },
        error: function(err) {
            console.log("Error:" + err);
        }
    });
});