// JS for Event Analysis Page

var timeFormat = 'YYYY-MM-DD'; // timeFormat is used by graph and data table

var color = Chart.helpers.color; // chart.js colors

var chart; // chart variable

var data_table_array = [] // array to store values of data table

// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

Chart.defaults.global.elements.line.tension = 0; // tension of lines in line graph

// Initialize date selects, get graph data and plot graph
$(document).ready(function() {

    $('#graph-from-date').val(moment().subtract(15, 'days').toISOString().substr(0, 10));
    $('#graph-to-date').val(moment().subtract(1, 'days').toISOString().substr(0, 10));

    getEventData();

});

// Initialization of Data table 
var eventDataTable = $('#event-data-table').DataTable({
    searching: false,
    scrollX: false,
    data: data_table_array,
    columns: [
        { "width": "75%" },
        { "width": "25%" },
    ],
    columnDefs: [{ 'type': 'date', 'targets': [0], }],
    order: [
        [0, 'asc']
    ],
    lengthMenu: [
        [10, 25, 50, -1],
        [10, 25, 50, "All"]
    ]
});

// Chart config 
var config = {
    type: 'bar',
    data: {
        datasets: [{
            label: 'Unique Visits',
            backgroundColor: color('rgb(78,115,223)').alpha(0.8).rgbString(),
            borderColor: 'rgb(78,115,223)',
            fill: false,
            data: [],
        }]
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: ''
        },
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    parser: timeFormat,
                    unit: 'day',
                    tooltipFormat: 'll',
                },
                display: true,
                scaleLabel: {
                    display: true,
                },
                ticks: {
                    major: {
                        fontStyle: 'bold',
                        fontColor: '#FF0000'
                    }
                },
                gridLines: {
                    display: true,
                    offsetGridLines: true
                },
                offset: true,
            }],
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    maxTicksLimit: 5,
                    padding: 0,
                },
                display: true,
            }]
        }
    }
};


// Function used to redraw chart after datasets chage
function redrawChart() {
    //if we already have a chart destroy it then carry on as normal
    if (chart) {

        chart.destroy();

    }

    var w = $("#chart-area").width();
    var c = document.getElementById("event-chart");

    c.width = w;
    c.height = w / 2;

    $("#chart_canvas").css("width", w);
    $("#chart_canvas").css("height", w / 2);

    var chart_canvas = document.getElementById("event-chart").getContext("2d");
    chart = new Chart(chart_canvas, config)
};


// Getting chart data from server
function getEventData() {

    fromDate = $('#graph-from-date').val();
    toDate = $('#graph-to-date').val();
    path = $('#path').html();

    $.ajax({
        type: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': window.CSRF_TOKEN,
            'Accept': 'application/json'
        },
        data: JSON.stringify({
            path: path,
            from: fromDate,
            to: toDate,
        }),
        url: "/dashboard/event_graph_data/",
        success: function(data) {

            // Parsing the data
            data = JSON.parse(data);

            // Discarding previous data from arrays
            config.data.datasets[0].data.length = 0
            data_table_array.length = 0

            // Inserting data to data_table_array and graph_data_array
            data.forEach((key, value) => {

                config.data.datasets[0].data.push({
                    'x': moment(key.date).format(timeFormat),
                    'y': key.unique_visits,
                });

                data_table_array.push([
                    moment(key.date).format('dddd MMMM Do YYYY'),
                    key.unique_visits,
                ]);
            });

            data_table_array.reverse();

            // Clearing the DataTable and adding rows with new data
            eventDataTable.clear().rows.add(data_table_array).draw();

            // Redrawing chart after data updation
            redrawChart();

        },
        error: function(err) {
            console.log("Error:" + err);
        }
    });
}

// Change chart type and values according to chart-select
$('#chart-select').on('change', function() {

    var chart_type = $('#chart-select').val();
    config.type = chart_type;

    if (chart_type == 'line') {

        // Reset the gridline in case of bar chart
        config.options.scales.xAxes[0].gridLines.offsetGridLines = false;
        config.options.scales.xAxes[0].offset = false

    } else {

        // Offset the gridline in case of bar chart
        config.options.scales.xAxes[0].gridLines.offsetGridLines = true;
        config.options.scales.xAxes[0].offset = true

    }

    // Update chart to accomodate changes
    chart.update();

});


// Change dates on graph-left-jump button click
$("#graph-left-jump").click(function() {

    var from_date = new Date($('#graph-from-date').val());
    var to_date = new Date($('#graph-to-date').val());

    var new_from_date = from_date;
    var new_to_date = to_date;

    new_from_date.setDate(new_from_date.getDate() - 7);
    new_to_date.setDate(new_to_date.getDate() - 7);

    $("#graph-from-date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph-to-date").val(new_to_date.toISOString().substr(0, 10));

    getEventData();

});

// Change dates on graph-right-jump button click
$("#graph-right-jump").click(function() {

    var from_date = new Date($('#graph-from-date').val());
    var to_date = new Date($('#graph-to-date').val());

    var new_from_date = from_date;
    var new_to_date = to_date;

    new_from_date.setDate(new_from_date.getDate() + 7);
    new_to_date.setDate(new_to_date.getDate() + 7);


    if (new_to_date > moment()) {
        return;
    }

    $("#graph-from-date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph-to-date").val(new_to_date.toISOString().substr(0, 10));

    getEventData();

});

// Change dates on graph-left-crawl button click
$("#graph-left-crawl").click(function() {

    var from_date = new Date($('#graph-from-date').val());
    var to_date = new Date($('#graph-to-date').val());

    var new_from_date = from_date;
    var new_to_date = to_date;

    new_from_date.setDate(new_from_date.getDate() - 1);
    new_to_date.setDate(new_to_date.getDate() - 1);

    $("#graph-from-date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph-to-date").val(new_to_date.toISOString().substr(0, 10));

    getEventData();

});

// Change dates on graph-right-crawl button click
$("#graph-right-crawl").click(function() {

    var from_date = new Date($('#graph-from-date').val());
    var to_date = new Date($('#graph-to-date').val());

    var new_from_date = from_date;
    var new_to_date = to_date;

    new_from_date.setDate(new_from_date.getDate() + 1);
    new_to_date.setDate(new_to_date.getDate() + 1);

    if (new_to_date > moment()) {
        return;
    }

    $("#graph-from-date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph-to-date").val(new_to_date.toISOString().substr(0, 10));

    getEventData();

});

// Change dates on graph-zoom-out button click
$("#graph-zoom-out").click(function() {

    var from_date = new Date($('#graph-from-date').val());
    var to_date = new Date($('#graph-to-date').val());

    var new_from_date = from_date;
    var new_to_date = to_date;
    new_from_date.setDate(new_from_date.getDate() - 1);
    new_to_date.setDate(new_to_date.getDate() + 1);

    if (new_to_date > moment()) {

        new_from_date.setDate(new_from_date.getDate() - 1);
        new_to_date = moment();

    }

    $("#graph-from-date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph-to-date").val(new_to_date.toISOString().substr(0, 10));

    getEventData();

});

// Change dates on graph-zoom-in button click
$("#graph-zoom-in").click(function() {

    var from_date = new Date($('#graph-from-date').val());
    var to_date = new Date($('#graph-to-date').val());

    var new_from_date = from_date;
    var new_to_date = to_date;

    new_from_date.setDate(new_from_date.getDate() + 1);
    new_to_date.setDate(new_to_date.getDate() - 1);

    if (new_from_date >= new_to_date) {
        return;
    }

    $("#graph-from-date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph-to-date").val(new_to_date.toISOString().substr(0, 10));

    getEventData();

});

// Function to download csv generated from Datatable data
function downloadCSV(csv, filename) {
    var csvFile;
    var downloadLink;

    // CSV file
    csvFile = new Blob([csv], { type: "text/csv" });

    // Download link
    downloadLink = document.createElement("a");

    // File name
    downloadLink.download = filename;

    // Create a link to the file
    downloadLink.href = window.URL.createObjectURL(csvFile);

    // Hide download link
    downloadLink.style.display = "none";

    // Add the link to DOM
    document.body.appendChild(downloadLink);

    // Click download link
    downloadLink.click();
}

// Function to generate csv from Datatable data
function exportTableToCSV(filename) {
    var csv = [];
    var rows = document.querySelectorAll("table tr");

    for (var i = 0; i < rows.length; i++) {
        var row = [],
            cols = rows[i].querySelectorAll("td, th");

        for (var j = 0; j < cols.length; j++)
            row.push(cols[j].innerText);

        csv.push(row.join(","));
    }

    // Download CSV file
    downloadCSV(csv.join("\n"), filename);
}