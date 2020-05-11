// JS for Event Analysis Page

var timeFormat = 'YYYY-MM-DD'; // timeFormat is used by graph and data table

// arrays to store different values used for plotting the graph
var page_views_array = []
var unique_visits_array = []
var returning_visits_array = []
var graph_data_table_array = []

var color = Chart.helpers.color; // chart.js colors

var data_summary_type = 'daily'; // will hold values like 'daily', 'monthly, 'yearly', etc

var chart; // chart variable

// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

Chart.defaults.global.elements.line.tension = 0; // tension of lines in line graph

$(document).ready(function() {
    $('#graph-from-date').val(moment().subtract(10, 'days').toISOString().substr(0, 10));
    $('#graph-to-date').val(moment().toISOString().substr(0, 10));
});


// Getting chart data from server
function getEventData() {

    fromDate = $('#graph-from-date').val()
    toDate = $('#graph-to-date').val()

    $.ajax({
        type: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': window.CSRF_TOKEN,
            'Accept': 'application/json'
        },
        data: JSON.stringify({
            from: fromDate,
            to: toDate,
        }),
        url: "/dashboard/events_data/",
        success: function(data) {

            // Parsing the data
            data = JSON.parse(data);

            data_table_array = []

            // Inserting data to data_table_array
            data.forEach((key, value) => {
                data_table_array.push([
                    key.event_name,
                    key.unique_visits,
                ])
            });

        },
        error: function(err) {
            console.log("Error:" + err);
        }
    });
}