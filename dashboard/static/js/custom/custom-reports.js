// JS for Reports page

// For tabs

//For tile-1
$("#tile-1 .nav-tabs a").click(function() {
    var position = $(this).parent().position();
    var width = $(this).parent().width();
    $("#tile-1 .slider").css({ "left": +position.left, "width": width });
});

var actWidth1 = $("#tile-1 .nav-tabs").find(".active").parent("li").width();
var actPosition1 = $("#tile-1 .nav-tabs .active").position();

$("#tile-1 .slider").css({ "left": +actPosition1.left, "width": actWidth1 });

//For tile-2
$("#tile-2 .nav-tabs a").click(function() {
    var position = $(this).parent().position();
    var width = $(this).parent().width();
    $("#tile-2 .slider").css({ "left": +position.left, "width": width });
});

var actWidth2 = $("#tile-2 .nav-tabs").find(".active").parent("li").width();
var actPosition2 = $("#tile-2 .nav-tabs .active").position();

$("#tile-2 .slider").css({ "left": +actPosition2.left, "width": actWidth2 });

//For tile-3
$("#tile-3 .nav-tabs a").click(function() {
    var position = $(this).parent().position();
    var width = $(this).parent().width();
    $("#tile-3 .slider").css({ "left": +position.left, "width": width });
});

var actWidth2 = $("#tile-3 .nav-tabs").find(".active").parent("li").width();
var actPosition2 = $("#tile-3 .nav-tabs .active").position();

$("#tile-3 .slider").css({ "left": +actPosition2.left, "width": actWidth2 });

//For tile-4
$("#tile-4 .nav-tabs a").click(function() {
    var position = $(this).parent().position();
    var width = $(this).parent().width();
    $("#tile-4 .slider").css({ "left": +position.left, "width": width });
});

var actWidth2 = $("#tile-4 .nav-tabs").find(".active").parent("li").width();
var actPosition2 = $("#tile-4 .nav-tabs .active").position();

$("#tile-4 .slider").css({ "left": +actPosition2.left, "width": actWidth2 });

// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

var chart;

// Pie chart config
config = {
    type: 'pie',
    data: {
        labels: ["Referring Websites", "Search Traffic", "Direct Traffic"],
        datasets: [{
            data: [10, 20, 70],
            backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
            hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf'],
            hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
    },
    options: {
        maintainAspectRatio: false,
        tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: true,
            caretPadding: 10,
            callbacks: {
                label: function(tooltipItem, data) {
                    var dataset = data.datasets[tooltipItem.datasetIndex];
                    var meta = dataset._meta[Object.keys(dataset._meta)[0]];
                    var total = meta.total;
                    var currentValue = dataset.data[tooltipItem.index];
                    var percentage = parseFloat((currentValue / total * 100).toFixed(1));
                    return ' (' + percentage + '%)';
                },
            }
        },
        legend: {
            display: true
        },
        cutoutPercentage: 50,
    },
}

// Function used to redraw chart after datasets chage
function drawChart() {
    //if we already have a chart destroy it then carry on as normal
    if (chart) {

        chart.destroy();

    }

    var w = $(".chart-pie").width();
    var c = document.getElementById("sourcesPieChart");

    c.width = w;
    c.height = w / 2;

    $("#chart_canvas").css("width", w);
    $("#chart_canvas").css("height", w / 2);

    var chart_canvas = document.getElementById("sourcesPieChart").getContext("2d");
    chart = new Chart(chart_canvas, config)
};

// Utility function prototype to truncate strings
String.prototype.trunc = function(length) {
    return this.length > length ? this.substring(0, length) + '&hellip;' : this;
};

// Utility function to format numbers (10000 to 10K)
function nFormatter(num) {

    if (num >= 1000000000) {

        return (num / 1000000000).toFixed(1).replace(/\.0$/, '') + 'B';

    }
    if (num >= 1000000) {

        return (num / 1000000).toFixed(1).replace(/\.0$/, '') + 'M';

    }
    if (num >= 1000) {

        return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'K';

    }

    return num;

}

// Ajax get data of reports
$(document).ready(function() {
    $(".fa-spinner").show();
    $.ajax({
        type: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': window.CSRF_TOKEN,
            'Accept': 'application/json'
        },
        url: "/dashboard/reports_stats/",
        success: function(data) {

            $(".fa-spinner").hide();

            // Parsing the data
            region_stats = JSON.parse(data.region_stats);
            city_stats = JSON.parse(data.city_stats);
            total_page_views = JSON.parse(data.total_page_views);

            foss_stats = JSON.parse(data.foss_stats);
            total_foss_page_views = JSON.parse(data.total_foss_page_views);
            events_stats = JSON.parse(data.events_stats);
            total_events_page_views = JSON.parse(data.total_events_page_views);

            browser_stats = JSON.parse(data.browser_stats);
            total_browser_page_views = JSON.parse(data.total_browser_page_views);
            platform_stats = JSON.parse(data.platform_stats);
            total_platform_page_views = JSON.parse(data.total_platform_page_views);
            os_stats = JSON.parse(data.os_stats);
            total_os_page_views = JSON.parse(data.total_os_page_views);

            sources_stats = data.sources_stats;
            came_from_stats = JSON.parse(data.came_from_stats);

            var region_table = $("#region-table tbody");
            var city_table = $("#city-table tbody");

            var foss_table = $("#foss-table tbody");
            var events_table = $("#events-table tbody");

            var browser_table = $('#browser-table tbody');
            var platform_table = $('#platform-table tbody');
            var os_table = $('#os-table tbody');

            var came_from_table = $('#came-from-table tbody');

            region_stats.forEach((key, value) => {
                region_table.append("<tr><td>" + key.fields.region + "</td><td><div class='progress progress-sm mb-2' style='margin-top: 0.7em;'><div class='progress-bar' role='progressbar' style='width: " + (key.fields.page_views / total_page_views).toFixed(2) * 100 + "%'aria-valuemin='0' aria-valuemax='100'></div></div></td><td class='text-primary'>" + ((key.fields.page_views / total_page_views) * 100).toFixed(2) + "%</td></tr>");
            });

            city_stats.forEach((key, value) => {
                city_table.append("<tr><td>" + key.fields.city + "</td><td><div class='progress progress-sm mb-2' style='margin-top: 0.7em;'><div class='progress-bar' role='progressbar' style='width: " + (key.fields.page_views / total_page_views).toFixed(2) * 100 + "%'aria-valuemin='0' aria-valuemax='100'></div></div></td><td class='text-primary'>" + ((key.fields.page_views / total_page_views) * 100).toFixed(2) + "%</td></tr>");
            });



            foss_stats.forEach((key, value) => {
                foss_table.append("<tr><td>" + key.foss_name + "</td><td><div class='progress progress-sm mb-2' style='margin-top: 0.7em;'><div class='progress-bar' role='progressbar' style='width: " + (key.page_views / total_foss_page_views).toFixed(2) * 100 + "%'aria-valuemin='0' aria-valuemax='100'></div></div></td><td class='text-primary'>" + ((key.page_views / total_foss_page_views) * 100).toFixed(2) + "%</td></tr>");
            });

            events_stats.forEach((key, value) => {
                events_table.append("<tr><td>" + key.event_name + "</td><td><div class='progress progress-sm mb-2' style='margin-top: 0.7em;'><div class='progress-bar' role='progressbar' style='width: " + (key.page_views / total_events_page_views).toFixed(2) * 100 + "%'aria-valuemin='0' aria-valuemax='100'></div></div></td><td class='text-primary'>" + ((key.page_views / total_events_page_views) * 100).toFixed(2) + "%</td></tr>");
            });



            browser_stats.forEach((key, value) => {
                browser_table.append("<tr><td>" + key.browser_type + "</td><td><div class='progress progress-sm mb-2' style='margin-top: 0.7em;'><div class='progress-bar' role='progressbar' style='width: " + (key.page_views / total_browser_page_views).toFixed(2) * 100 + "%'aria-valuemin='0' aria-valuemax='100'></div></div></td><td class='text-primary'>" + ((key.page_views / total_browser_page_views) * 100).toFixed(2) + "%</td></tr>");
            });

            platform_stats.forEach((key, value) => {
                platform_table.append("<tr><td>" + key.platform + "</td><td><div class='progress progress-sm mb-2' style='margin-top: 0.7em;'><div class='progress-bar' role='progressbar' style='width: " + (key.page_views / total_platform_page_views).toFixed(2) * 100 + "%'aria-valuemin='0' aria-valuemax='100'></div></div></td><td class='text-primary'>" + ((key.page_views / total_platform_page_views) * 100).toFixed(2) + "%</td></tr>");
            });

            os_stats.forEach((key, value) => {
                os_table.append("<tr><td>" + key.os + "</td><td><div class='progress progress-sm mb-2' style='margin-top: 0.7em;'><div class='progress-bar' role='progressbar' style='width: " + (key.page_views / total_os_page_views).toFixed(2) * 100 + "%'aria-valuemin='0' aria-valuemax='100'></div></div></td><td class='text-primary'>" + ((key.page_views / total_os_page_views) * 100).toFixed(2) + "%</td></tr>");
            });

            came_from_stats.forEach((key, value) => {
                came_from_table.append("<tr><td>" + key.referrer.trunc(50) + "<td class='text-primary'>" + nFormatter(key.page_views) + "</td></tr>");
            });

            // Change pie chart dataset
            config.data.datasets[0].data = [parseInt(sources_stats.referrer_page_views__sum), parseInt(sources_stats.search_page_views__sum), parseInt(sources_stats.direct_page_views__sum)];

            drawChart()
        },
        error: function(err) {
            $(".fa-spinner").hide();
            console.log("Error:" + err);
        }
    });
});