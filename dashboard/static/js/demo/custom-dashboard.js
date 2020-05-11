// JS for Dashboard Page

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

// Initialization after page load
$(document).ready(function() {

    $('.avg').each(function() {

        // Format counter values
        var value = $(this).html();
        $(this).html(nFormatter(value));

    });

    // Initialize date selects with initial values
    document.querySelector("#graph-to-date").value = moment().toISOString().substr(0, 10);
    document.querySelector("#graph-from-date").value = moment().subtract(7, 'days').toISOString().substr(0, 10);

    var week_of_year = moment().isoWeek();
    var year = moment().year();

    // Fill options of Week selects
    for (var i = 1; i <= 52; i++) {

        text = 'Week ' + i;
        value = i;

        // If i is the week of year make it selected otherwise not
        if (i == week_of_year) {

            $('#graph-to-week').append(`<option value="${value}" selected> ${text} </option>`);

        } else {

            $('#graph-to-week').append(`<option value="${value}"> ${text} </option>`);

        }

        // If current week_of_year is less than 5, make from_week = 52 - week_of_year 
        if ((week_of_year - 4) < 1) {

            value = 52 - week_of_year;
            text = 'Week ' + value;

        }

        if (i == (week_of_year - 4)) {

            $('#graph-from-week').append(`<option value="${value}" selected> ${text} </option>`);

        } else {

            $('#graph-from-week').append(`<option value="${value}"> ${text} </option>`);

        }
    }

    // If current week_of_year is less than 5, subtract 1 from from_year
    if ((week_of_year - 4) < 1) {

        year -= 1;

    }

    // Set Year values 
    $('#graph-from-year').val(year);
    $('#graph-to-year').val(moment().year());

    // Get graph data after values are set
    getGraphData();

});

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

// Function used to redraw chart after datasets chage
function redrawChart() {
    //if we already have a chart destroy it then carry on as normal
    if (chart) {

        chart.destroy();

    }

    var w = $("#chart-area").width();
    var c = document.getElementById("my-chart");

    c.width = w;
    c.height = w / 2;

    $("#chart_canvas").css("width", w);
    $("#chart_canvas").css("height", w / 2);

    var chart_canvas = document.getElementById("my-chart").getContext("2d");
    chart = new Chart(chart_canvas, config)
};

// Utility function used to add 0 before numbers of numbers are less than 10
function minTwoDigits(n) {
    return (n < 10 ? '0' : '') + n;
}

// Chart config 
var config = {
    type: 'bar',
    data: {
        datasets: [{
            label: 'Page Views',
            backgroundColor: color('rgb(78,115,223)').alpha(0.8).rgbString(),
            borderColor: 'rgb(78,115,223)',
            fill: false,
            data: page_views_array,
        }, {
            label: 'Unique Visits',
            backgroundColor: color('rgb(28,200,138)').alpha(0.8).rgbString(),
            borderColor: 'rgb(28,200,138)',
            fill: false,
            data: unique_visits_array,
        }, {
            label: 'Returning Visits',
            backgroundColor: color('rgb(246,194,62)').alpha(0.8).rgbString(),
            borderColor: 'rgb(246,194,62)',
            fill: false,
            data: returning_visits_array,
        }, ]
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
                    isoWeekday: true,
                    displayFormats: {
                        day: 'll',
                        week: 'YYYY-[W]WW',
                        month: 'MMM YYYY',
                        year: 'YYYY'
                    }
                },
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Date'
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
                    padding: 10,
                },
                display: true,
            }]
        }
    }
};

// Initialization of Data table 
var graphDataTable = $('#graph-data-table').DataTable({
    searching: false,
    scrollX: false,
    data: graph_data_table_array,
    columns: [
        { "width": "40%" },
        { "width": "15%" },
        { "width": "15%" },
        { "width": "15%" },
        { "width": "15%" },
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

// Getting chart data from server
function getGraphData() {

    // fromDate and toDate hold date like {'week': '15', 'year': '2020'} if data_summary_type is weekly 
    //  else like '2020-05-01'
    if (data_summary_type == 'weekly') {

        fromDate = {
            week: $('#graph-from-week').val(),
            year: $('#graph-from-year').val()
        }

        toDate = {
            week: $('#graph-to-week').val(),
            year: $('#graph-to-year').val()
        }


    } else {

        fromDate = $('#graph-from-date').val();
        toDate = $('#graph-to-date').val();

    }

    $.ajax({
        type: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': window.CSRF_TOKEN,
            'Accept': 'application/json'
        },
        data: JSON.stringify({
            data_summary_type: data_summary_type,
            from: fromDate,
            to: toDate,
        }),
        url: "/dashboard/graph_data/",
        success: function(data) {

            // Parsing the data
            data_for_graph = JSON.parse(data.stats);
            avg_stats = JSON.parse(data.avg_stats);

            // Sending data for graph to be parsed into different chart dataset arrays
            fillDataToChartArrays(data_for_graph);

            // Call to redraw function to redraw the chart
            redrawChart();

            // Clearing the DataTable and adding rows with new data
            graphDataTable.clear().rows.add(graph_data_table_array).draw();
        },
        error: function(err) {
            console.log("Error:" + err);
        }
    });
}

// Function used to fill chart datasets arrays with data
function fillDataToChartArrays(data) {

    page_views_array.length = 0
    unique_visits_array.length = 0
    returning_visits_array.length = 0
    graph_data_table_array.length = 0

    if (data_summary_type == 'daily') {

        data.forEach((key, value) => {

            page_views_array.push({
                'x': moment(key.fields.date).format(timeFormat), // time
                'y': key.fields.page_views, // value
            })

            unique_visits_array.push({
                'x': moment(key.fields.date).format(timeFormat),
                'y': key.fields.unique_visits,
            })

            returning_visits_array.push({
                'x': moment(key.fields.date).format(timeFormat),
                'y': key.fields.returning_visits,
            })

            graph_data_table_array.push([
                moment(key.fields.date).format('dddd MMMM Do YYYY'),
                key.fields.page_views,
                key.fields.unique_visits,
                key.fields.first_time_visits,
                key.fields.returning_visits,
            ])

        });

    } else if (data_summary_type == 'weekly') {

        data.forEach((key, value) => {
            page_views_array.push({
                // Coverting week and year to format like 2020-W4-1 so that it can be parsed into moment object
                // Chart js takes only moment objects for time.
                'x': moment(key.fields.year.toString() + '-W' + minTwoDigits(key.fields.week_of_year.toString()) + '-1'),
                'y': key.fields.page_views,
            })
            unique_visits_array.push({
                // Coverting week and year to format like 2020-W4-1 so that it can be parsed into moment object
                // Chart js takes only moment objects for time.
                'x': moment(key.fields.year.toString() + '-W' + minTwoDigits(key.fields.week_of_year.toString()) + '-1'),
                'y': key.fields.unique_visits,
            })
            returning_visits_array.push({
                // Coverting week and year to format like 2020-W4-1 so that it can be parsed into moment object
                // Chart js takes only moment objects for time.
                'x': moment(key.fields.year.toString() + '-W' + minTwoDigits(key.fields.week_of_year.toString()) + '-1'),
                'y': key.fields.returning_visits,
            })
            graph_data_table_array.push([
                // coverting week and year to format like 2020-W4-1 so that it can be parsed into moment object for DataTable
                moment(key.fields.year.toString() + '-W' + minTwoDigits(key.fields.week_of_year.toString()) + '-1').format(timeFormat),
                key.fields.page_views,
                key.fields.unique_visits,
                key.fields.first_time_visits,
                key.fields.returning_visits,
            ])
        });

    } else if (data_summary_type == 'monthly') {

        data.forEach((key, value) => {
            // Coverting month and year to format like 2020-04 so that it can be parsed into moment object
            // Chart js takes only moment objects for time.
            page_views_array.push({
                'x': moment(key.fields.year.toString() + '-' + minTwoDigits(key.fields.month_of_year.toString())),
                'y': key.fields.page_views,
            })
            unique_visits_array.push({
                // Coverting month and year to format like 2020-04 so that it can be parsed into moment object
                // Chart js takes only moment objects for time.
                'x': moment(key.fields.year.toString() + '-' + minTwoDigits(key.fields.month_of_year.toString())),
                'y': key.fields.unique_visits,
            })
            returning_visits_array.push({
                // Coverting month and year to format like 2020-04 so that it can be parsed into moment object
                // Chart js takes only moment objects for time.
                'x': moment(key.fields.year.toString() + '-' + minTwoDigits(key.fields.month_of_year.toString())),
                'y': key.fields.returning_visits,
            })
            graph_data_table_array.push([
                // Coverting month and year to format like 2020-04 so that it can be parsed into moment object for DataTable
                moment(key.fields.year.toString() + '-' + minTwoDigits(key.fields.month_of_year.toString())).format(timeFormat),
                key.fields.page_views,
                key.fields.unique_visits,
                key.fields.first_time_visits,
                key.fields.returning_visits,
            ])
        });

    } else if (data_summary_type == 'yearly') {

        data.forEach((key, value) => {
            page_views_array.push({
                // Coverting year to format like 2020-01 so that it can be parsed into moment object
                // Chart js takes only moment objects for time.
                'x': moment(key.fields.year.toString() + '-01'),
                'y': key.fields.page_views,
            })
            unique_visits_array.push({
                // Coverting year to format like 2020-01 so that it can be parsed into moment object
                // Chart js takes only moment objects for time.
                'x': moment(key.fields.year.toString() + '-01'),
                'y': key.fields.unique_visits,
            })
            returning_visits_array.push({
                // Coverting year to format like 2020-01 so that it can be parsed into moment object
                // Chart js takes only moment objects for time.
                'x': moment(key.fields.year.toString() + '-01'),
                'y': key.fields.returning_visits,
            })
            graph_data_table_array.push([
                // Coverting year to format like 2020-01 so that it can be parsed into moment object for DataTable
                moment(key.fields.year.toString() + '-01').format('YYYY'),
                key.fields.page_views,
                key.fields.unique_visits,
                key.fields.first_time_visits,
                key.fields.returning_visits,
            ])
        });
    }

    // reversing the graph_data_table_array array so DataTabel displays nearest date first
    graph_data_table_array.reverse()

}

// Change chart type and values according to chart-select
$('#chart-select').on('change', function() {

    var chart_type = $('#chart-select').val();
    config.type = chart_type;

    if (chart_type == 'line') {

        config.options.scales.xAxes[0].gridLines.offsetGridLines = false;
        config.options.scales.xAxes[0].offset = false

    } else {

        // Offset the gridline in case of bar chart
        config.options.scales.xAxes[0].gridLines.offsetGridLines = true;
        config.options.scales.xAxes[0].offset = true

    }

    // update chart to accomodate changes
    chart.update();

});

// Change different values on granularity change ('daily', 'monthly', etc)
$('#summary-granularity-trigger').on('change', function() {

    data_summary_type = $('#summary-granularity-trigger').val();

    updateAverageCounters();

    // Reset graph-to-date to current date
    $("#graph-to-date").val(moment().toISOString().substr(0, 10));

    if (data_summary_type == 'daily') {

        timeFormat = 'YYYY-MM-DD';

        // Reset graph-to-date to current date - 7 days
        $("#graph-from-date").val(moment().subtract(7, 'days').toISOString().substr(0, 10));

        $('#date-select-div').show();
        $('#week-select-div').hide();

        // Change X-axis time unit
        config.options.scales.xAxes[0].time.unit = 'day';

    } else if (data_summary_type == 'weekly') {

        timeFormat = 'YYYY-[W]WW';

        $('#date-select-div').hide();
        $('#week-select-div').show();

        // Change X-axis time unit
        config.options.scales.xAxes[0].time.unit = 'week';

    } else if (data_summary_type == 'monthly') {

        timeFormat = 'MMM YYYY'

        $('#date-select-div').show();
        $('#week-select-div').hide();

        // Reset graph-to-date to current date - 2 months
        $("#graph-from-date").val(moment().startOf('month').subtract(2, 'months').toISOString().substr(0, 10));

        // Change X-axis time unit
        config.options.scales.xAxes[0].time.unit = 'month';

    } else if (data_summary_type == 'yearly') {

        timeFormat = 'YYYY'

        $('#date-select-div').show();
        $('#week-select-div').hide();

        // Reset graph-to-date to current date - 2 years
        $("#graph-from-date").val(moment().startOf('year').subtract(2, 'years').toISOString().substr(0, 10));

        // Change X-axis time unit
        config.options.scales.xAxes[0].time.unit = 'year';

    }

    // Fetch graph data according to changed values
    getGraphData();

});

// Change dates and weeks on graph-left-jump button click
$("#graph-left-jump").click(function() {

    var from_date = new Date($('#graph-from-date').val());
    var to_date = new Date($('#graph-to-date').val());

    var new_from_date = from_date;
    var new_to_date = to_date;

    if (data_summary_type == 'daily') {

        new_from_date.setDate(new_from_date.getDate() - 7);
        new_to_date.setDate(new_to_date.getDate() - 7);

    } else if (data_summary_type == 'weekly') {

        var from_week_select = $('#graph-from-week');
        var to_week_select = $('#graph-to-week');

        var from_week = from_week_select.val();
        var to_week = to_week_select.val();

        var new_from_week = parseInt(from_week) - 1;
        var new_to_week = parseInt(to_week) - 1;

        if (new_from_week < 1) {

            new_from_week = 52;
            var year = $('#graph-from-year').val();
            $('#graph-from-year').val(parseInt(year) - 1);

        }

        if (new_to_week < 1) {

            new_to_week = 52;
            var year = $('#graph-to-year').val();
            $('#graph-to-year').val(parseInt(year) - 1);

        }

        from_week_select.val(new_from_week);
        to_week_select.val(new_to_week);


    } else if (data_summary_type == 'monthly') {

        new_from_date.setMonth(new_from_date.getMonth() - 1);
        new_to_date.setMonth(new_to_date.getMonth() - 1);

    } else {

        new_from_date.setFullYear(new_from_date.getFullYear() - 1);
        new_to_date.setFullYear(new_to_date.getFullYear() - 1);

    }

    $("#graph-from-date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph-to-date").val(new_to_date.toISOString().substr(0, 10));
    4

    getGraphData();

});

// Change dates and weeks on graph-right-jump button click
$("#graph-right-jump").click(function() {

    var from_date = new Date($('#graph-from-date').val());
    var to_date = new Date($('#graph-to-date').val());

    var new_from_date = from_date;
    var new_to_date = to_date;

    if (data_summary_type == 'daily') {

        new_from_date.setDate(new_from_date.getDate() + 7);
        new_to_date.setDate(new_to_date.getDate() + 7);

    } else if (data_summary_type == 'weekly') {

        var from_week_select = $('#graph-from-week');
        var to_week_select = $('#graph-to-week');

        var from_week = from_week_select.val();
        var to_week = to_week_select.val();

        var new_from_week = parseInt(from_week) + 1;
        var new_to_week = parseInt(to_week) + 1;

        if (new_from_week > 52) {
            new_from_week = 1;
            var year = $('#graph-from-year').val();
            $('#graph-from-year').val(parseInt(year) + 1);
        }

        if (new_to_week > 52) {
            new_to_week = 1;
            var year = $('#graph-to-year').val();
            $('#graph-to-year').val(parseInt(year) + 1);
        }

        if (new_to_week > moment().isoWeek()) {
            return;
        }

        from_week_select.val(new_from_week);
        to_week_select.val(new_to_week);

    } else if (data_summary_type == 'monthly') {

        new_from_date.setMonth(new_from_date.getMonth() + 1);
        new_to_date.setMonth(new_to_date.getMonth() + 1);

    } else {

        new_from_date.setFullYear(new_from_date.getFullYear() + 1);
        new_to_date.setFullYear(new_to_date.getFullYear() + 1);

    }

    if (new_to_date > moment()) {
        return;
    }

    $("#graph-from-date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph-to-date").val(new_to_date.toISOString().substr(0, 10));

    getGraphData();

});

// Change dates and weeks on graph-left-crawl button click
$("#graph-left-crawl").click(function() {

    var from_date = new Date($('#graph-from-date').val());
    var to_date = new Date($('#graph-to-date').val());

    var new_from_date = from_date;
    var new_to_date = to_date;

    if (data_summary_type == 'daily') {

        new_from_date.setDate(new_from_date.getDate() - 1);
        new_to_date.setDate(new_to_date.getDate() - 1);

    } else if (data_summary_type == 'weekly') {

        var from_week_select = $('#graph-from-week');
        var to_week_select = $('#graph-to-week');

        var from_week = from_week_select.val();
        var to_week = to_week_select.val();

        var new_from_week = parseInt(from_week) - 1;
        var new_to_week = parseInt(to_week) - 1;

        if (new_from_week < 1) {
            new_from_week = 52;
            var year = $('#graph-from-year').val();
            $('#graph-from-year').val(parseInt(year) - 1);
        }

        if (new_to_week < 1) {
            new_to_week = 52;
            var year = $('#graph-to-year').val();
            $('#graph-to-year').val(parseInt(year) - 1);
        }

        from_week_select.val(new_from_week);
        to_week_select.val(new_to_week);


    } else if (data_summary_type == 'monthly') {

        new_from_date.setMonth(new_from_date.getMonth() - 1);
        new_to_date.setMonth(new_to_date.getMonth() - 1);

    } else {

        new_from_date.setFullYear(new_from_date.getFullYear() - 1);
        new_to_date.setFullYear(new_to_date.getFullYear() - 1);

    }

    if (new_to_date > moment()) {
        return;
    }

    $("#graph-from-date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph-to-date").val(new_to_date.toISOString().substr(0, 10));

    getGraphData();

});

// Change dates and weeks on graph-right-crawl button click
$("#graph-right-crawl").click(function() {

    var from_date = new Date($('#graph-from-date').val());
    var to_date = new Date($('#graph-to-date').val());

    var new_from_date = from_date;
    var new_to_date = to_date;

    if (data_summary_type == 'daily') {

        new_from_date.setDate(new_from_date.getDate() + 1);
        new_to_date.setDate(new_to_date.getDate() + 1);

    } else if (data_summary_type == 'weekly') {

        var from_week_select = $('#graph-from-week');
        var to_week_select = $('#graph-to-week');

        var from_week = from_week_select.val();
        var to_week = to_week_select.val();

        var new_from_week = parseInt(from_week) + 1;
        var new_to_week = parseInt(to_week) + 1;

        if (new_from_week > 52) {
            new_from_week = 1;
            var year = $('#graph-from-year').val();
            $('#graph-from-year').val(parseInt(year) + 1);
        }

        if (new_to_week > 52) {
            new_to_week = 1;
            var year = $('#graph-to-year').val();
            $('#graph-to-year').val(parseInt(year) + 1);
        }

        if (new_to_week > moment().isoWeek()) {
            return;
        }

        from_week_select.val(new_from_week);
        to_week_select.val(new_to_week);

    } else if (data_summary_type == 'monthly') {

        new_from_date.setMonth(new_from_date.getMonth() + 1);
        new_to_date.setMonth(new_to_date.getMonth() + 1);

    } else {

        new_from_date.setFullYear(new_from_date.getFullYear() + 1);
        new_to_date.setFullYear(new_to_date.getFullYear() + 1);

    }

    if (new_to_date > moment()) {
        return;
    }

    $("#graph-from-date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph-to-date").val(new_to_date.toISOString().substr(0, 10));

    getGraphData();

});

// Change dates and weeks on graph-zoom-out button click
$("#graph-zoom-out").click(function() {

    var from_date = new Date($('#graph-from-date').val());
    var to_date = new Date($('#graph-to-date').val());

    var new_from_date = from_date;
    var new_to_date = to_date;

    if (data_summary_type == 'daily') {

        new_from_date.setDate(new_from_date.getDate() - 1);
        new_to_date.setDate(new_to_date.getDate() + 1);

        if (new_to_date > moment()) {

            new_from_date.setDate(new_from_date.getDate() - 1);
            new_to_date = moment();

        }

    } else if (data_summary_type == 'weekly') {

        var from_week_select = $('#graph-from-week');
        var to_week_select = $('#graph-to-week');

        var from_week = from_week_select.val();
        var to_week = to_week_select.val();

        var new_from_week = parseInt(from_week) - 1;
        var new_to_week = parseInt(to_week) + 1;

        if (new_to_week >= moment().isoWeek()) {

            new_to_week = to_week;
            new_from_week -= 1;

        }

        if (new_from_week > 52) {

            new_from_week = 1;
            var year = $('#graph-from-year').val();
            $('#graph-from-year').val(parseInt(year) + 1);

        }

        if (new_to_week > 52) {

            new_to_week = 1;
            var year = $('#graph-to-year').val();
            $('#graph-to-year').val(parseInt(year) + 1);

        }


        if (new_from_week < 1) {

            new_from_week = 52;
            var year = $('#graph-from-year').val();
            $('#graph-from-year').val(parseInt(year) - 1);

        }


        if (new_to_week < 1) {

            new_to_week = 52;
            var year = $('#graph-to-year').val();
            $('#graph-to-year').val(parseInt(year) - 1);

        }

        from_week_select.val(new_from_week);
        to_week_select.val(new_to_week);

    } else if (data_summary_type == 'monthly') {

        new_from_date.setMonth(new_from_date.getMonth() - 1);
        new_to_date.setMonth(new_to_date.getMonth() + 1);

        if (new_to_date > moment()) {

            new_from_date.setDate(new_from_date.getMonth() - 1);
            new_to_date = moment();

        }

    } else {

        new_from_date.setFullYear(new_from_date.getFullYear() - 1);
        new_to_date.setFullYear(new_to_date.getFullYear() + 1);

        if (new_to_date > moment()) {

            new_from_date.setFullYear(new_from_date.getFullYear() - 1);
            new_to_date = moment();

        }

    }

    $("#graph-from-date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph-to-date").val(new_to_date.toISOString().substr(0, 10));

    getGraphData();

});

// Change dates and weeks on graph-zoom-in button click
$("#graph-zoom-in").click(function() {

    var from_date = new Date($('#graph-from-date').val());
    var to_date = new Date($('#graph-to-date').val());

    var new_from_date = from_date;
    var new_to_date = to_date;

    if (data_summary_type == 'daily') {

        new_from_date.setDate(new_from_date.getDate() + 1);
        new_to_date.setDate(new_to_date.getDate() - 1);

    } else if (data_summary_type == 'weekly') {

        var from_week_select = $('#graph-from-week');
        var to_week_select = $('#graph-to-week');

        var from_week = from_week_select.val();
        var to_week = to_week_select.val();

        var new_from_week = parseInt(from_week) + 1;
        var new_to_week = parseInt(to_week) - 1;

        if (new_from_week > 52) {
            new_from_week = 1;
            var year = $('#graph-from-year').val();
            $('#graph-from-year').val(parseInt(year) + 1);
        }

        if (new_to_week > 52) {
            new_to_week = 1;
            var year = $('#graph-to-year').val();
            $('#graph-to-year').val(parseInt(year) + 1);
        }


        if (new_from_week < 1) {
            new_from_week = 52;
            var year = $('#graph-from-year').val();
            $('#graph-from-year').val(parseInt(year) - 1);
        }


        if (new_to_week < 1) {
            new_to_week = 52;
            var year = $('#graph-to-year').val();
            $('#graph-to-year').val(parseInt(year) - 1);
        }

        if (new_from_week >= new_to_week && $('#graph-from-year').val() === $('#graph-to-year').val()) {
            return;
        }

        from_week_select.val(new_from_week);
        to_week_select.val(new_to_week);

    } else if (data_summary_type == 'monthly') {

        new_from_date.setMonth(new_from_date.getMonth() + 1);
        new_to_date.setMonth(new_to_date.getMonth() - 1);

    } else {

        new_from_date.setFullYear(new_from_date.getFullYear() + 1);
        new_to_date.setFullYear(new_to_date.getFullYear() - 1);

    }

    if (new_from_date >= new_to_date) {
        return;
    }

    $("#graph-from-date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph-to-date").val(new_to_date.toISOString().substr(0, 10));

    getGraphData();

});

// Update average counters according to granularity ('daily', 'mothly', etc)
function updateAverageCounters() {

    $(".granularity").each(function() {
        $(this).html(data_summary_type);
    });

    if (data_summary_type == 'daily') {

        $('.average-daily').each(function() {
            $(this).show();
        });

        $('.average-weekly').each(function() {
            $(this).hide();
        });

        $('.average-monthly').each(function() {
            $(this).hide();
        });

        $('.average-yearly').each(function() {
            $(this).hide();
        });

    } else if (data_summary_type == 'weekly') {

        $('.average-daily').each(function() {
            $(this).hide();
        });

        $('.average-weekly').each(function() {
            $(this).show();
        });

        $('.average-monthly').each(function() {
            $(this).hide();
        });

        $('.average-yearly').each(function() {
            $(this).hide();
        });

    } else if (data_summary_type == 'monthly') {

        $('.average-daily').each(function() {
            $(this).hide();
        });

        $('.average-weekly').each(function() {
            $(this).hide();
        });

        $('.average-monthly').each(function() {
            $(this).show();
        });

        $('.average-yearly').each(function() {
            $(this).hide();
        });

    } else {

        $('.average-daily').each(function() {
            $(this).hide();
        });

        $('.average-weekly').each(function() {
            $(this).hide();
        });

        $('.average-monthly').each(function() {
            $(this).hide();
        });

        $('.average-yearly').each(function() {
            $(this).show();
        });

    }

}

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