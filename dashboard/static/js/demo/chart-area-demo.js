var timeFormat = 'YYYY-MM-DD';

page_views_array = []
unique_visits_array = []
returning_visits_array = []
graph_data_table_array = []

var color = Chart.helpers.color; // chart.js colors

var data_summary_type = 'daily'

var chart;

// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';
Chart.defaults.global.elements.line.tension = 0;

function redrawChart() {
    //if we already have a chart destroy it then carry on as normal
    if(chart)
    {
            chart.destroy();
    }
    var w = $("#chart-area").width();
    var c = document.getElementById("my-chart");
    c.width = w;
    c.height = w/2;
    $("#chart_canvas").css("width", w);
    $("#chart_canvas").css("height", w/2);

    var chart_canvas = document.getElementById("my-chart").getContext("2d");
    chart= new Chart(chart_canvas, config)
};

function minTwoDigits(n) {
    return (n < 10 ? '0' : '') + n;
}

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}

var config = {
  type: 'bar',
  data: {
      datasets: [{
        label: 'Page Views',
        backgroundColor: color('rgb(78,115,223)').alpha(0.8).rgbString(),
        borderColor: 'rgb(78,115,223)',
        fill: false,
        data:page_views_array,
      },{
        label: 'Unique Visits',
        backgroundColor: color('rgb(28,200,138)').alpha(0.8).rgbString(),
        borderColor: 'rgb(28,200,138)',
        fill: false,
        data: unique_visits_array,
      },{
        label: 'Returning Visits',
        backgroundColor: color('rgb(246,194,62)').alpha(0.8).rgbString(),
        borderColor: 'rgb(246,194,62)',
        fill: false,
        data: returning_visits_array,
      },
    ]
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
                    week:'YYYY-[W]WW',
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
                callback: function(value, index, values) {
                  return number_format(value);
                }
            },
            display: true,
          }]
      }
  }
};


var graphDataTable = $('#graph-data-table').DataTable({
    searching: false,
    data: graph_data_table_array,
    columns: [
        { "width": "40%" },
        { "width": "15%" },
        { "width": "15%" },
        { "width": "15%" },
        { "width": "15%" },
      ],
    columnDefs: [ { 'type': 'date', 'targets': [0],  }],
    order: [[ 0, 'asc' ]],
});

// Getting chart data from server
function getGraphData(){ 

    if(data_summary_type == 'weekly') {

        fromDate = {
            week: $('#graph-from-week').val(),
            year: $('#graph-from-year').val()
        }

        toDate = {
            week: $('#graph-to-week').val(),
            year: $('#graph-to-year').val()
        }


    } else {

        fromDate = $('#graph-from-date').val()
        toDate = $('#graph-to-date').val()

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
            data = JSON.parse(data);

            fillDataToChartArrays(data)
            redrawChart();
            graphDataTable.clear().rows.add(graph_data_table_array).draw();
        },
        error: function(err) {
            console.log("Error:" + err);
        }
    });
}

function fillDataToChartArrays(data) {

    page_views_array.length = 0
    unique_visits_array.length = 0
    returning_visits_array.length = 0
    graph_data_table_array.length = 0

    if(data_summary_type == 'daily') {

        data.forEach((key, value) => {

            page_views_array.push({
                'x': moment(key.fields.date).format(timeFormat),
                'y': key.fields.page_views,
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
                moment(key.fields.date).format('dddd, MMMM Do, YYYY'),
                key.fields.page_views,
                key.fields.unique_visits,
                key.fields.first_time_visits,
                key.fields.returning_visits,
            ])

        });

    } else if(data_summary_type == 'weekly') {

        data.forEach((key, value) => {
            page_views_array.push({
                'x': moment(key.fields.year.toString() + '-W' + minTwoDigits(key.fields.week_of_year.toString()) + '-1'),
                'y': key.fields.page_views,
            })
            unique_visits_array.push({
                'x': moment(key.fields.year.toString() + '-W' + minTwoDigits(key.fields.week_of_year.toString()) + '-1'),
                'y': key.fields.unique_visits,
            })
            returning_visits_array.push({
                'x': moment(key.fields.year.toString() + '-W' + minTwoDigits(key.fields.week_of_year.toString()) + '-1'),
                'y': key.fields.returning_visits,
            })
            graph_data_table_array.push([
                moment(key.fields.year.toString() + '-W' + minTwoDigits(key.fields.week_of_year.toString()) + '-1').format(timeFormat),
                key.fields.page_views,
                key.fields.unique_visits,
                key.fields.first_time_visits,
                key.fields.returning_visits,
            ])
        });

    } else if(data_summary_type == 'monthly') {

        data.forEach((key, value) => {
            page_views_array.push({
                'x': moment(key.fields.year.toString() + '-' + minTwoDigits(key.fields.month_of_year.toString())),
                'y': key.fields.page_views,
            })
            unique_visits_array.push({
                'x': moment(key.fields.year.toString() + '-' + minTwoDigits(key.fields.month_of_year.toString())),
                'y': key.fields.unique_visits,
            })
            returning_visits_array.push({
                'x': moment(key.fields.year.toString() + '-' + minTwoDigits(key.fields.month_of_year.toString())),
                'y': key.fields.returning_visits,
            })
            graph_data_table_array.push([
                moment(key.fields.year.toString() + '-' + minTwoDigits(key.fields.month_of_year.toString())).format(timeFormat),
                key.fields.page_views,
                key.fields.unique_visits,
                key.fields.first_time_visits,
                key.fields.returning_visits,
            ])
        });

    } else if(data_summary_type == 'yearly') {

        data.forEach((key, value) => {
            page_views_array.push({
                'x': moment(key.fields.year.toString() + '-01'),
                'y': key.fields.page_views,
            })
            unique_visits_array.push({
                'x': moment(key.fields.year.toString() + '-01'),
                'y': key.fields.unique_visits,
            })
            returning_visits_array.push({
                'x': moment(key.fields.year.toString() + '-01'),
                'y': key.fields.returning_visits,
            })
            graph_data_table_array.push([
                moment(key.fields.year.toString()).format('YYYY'),
                key.fields.page_views,
                key.fields.unique_visits,
                key.fields.first_time_visits,
                key.fields.returning_visits,
            ])
        });
    }
    
    graph_data_table_array.reverse()
    
}

$('#chart-select').on('change', function() {
    var chart_type = $('#chart-select').val();
    config.type = chart_type;
    if(chart_type == 'line') {
        config.options.scales.xAxes[0].gridLines.offsetGridLines = false;
        config.options.scales.xAxes[0].offset = false
    } else {
        config.options.scales.xAxes[0].gridLines.offsetGridLines = true;
        config.options.scales.xAxes[0].offset = true
    }
    chart.update();
});

$('#summary-granularity-trigger').on('change', function() {

    data_summary_type = $('#summary-granularity-trigger').val();
    
    $("#graph-to-date").val(moment().toISOString().substr(0, 10));

    if (data_summary_type == 'daily') {
        
        timeFormat = 'YYYY-MM-DD';

        $("#graph-from-date").val(moment().subtract(7, 'days').toISOString().substr(0, 10));

        $('#date-select-div').show();
        $('#week-select-div').hide();

        config.options.scales.xAxes[0].time.unit = 'day';
        getGraphData();

    } else if (data_summary_type == 'weekly') {
        
        timeFormat = 'YYYY-[W]WW';
        
        $('#date-select-div').hide();
        $('#week-select-div').show();

        config.options.scales.xAxes[0].time.unit = 'week';

        getGraphData()

    } else if (data_summary_type == 'monthly') {

        timeFormat = 'MMM YYYY'

        $('#date-select-div').show();
        $('#week-select-div').hide();

        $("#graph-from-date").val(moment().startOf('month').subtract(2, 'months').toISOString().substr(0, 10));

        config.options.scales.xAxes[0].time.unit = 'month';

        getGraphData();
        
    } else if (data_summary_type == 'yearly') {

        timeFormat = 'YYYY'

        $('#date-select-div').show();
        $('#week-select-div').hide();

        $("#graph-from-date").val(moment().startOf('year').subtract(2, 'years').toISOString().substr(0, 10));

        config.options.scales.xAxes[0].time.unit = 'year';

        getGraphData();

    }
});

$(document).ready( function () {

    document.querySelector("#graph-to-date").value = moment().toISOString().substr(0, 10);
    document.querySelector("#graph-from-date").value = moment().subtract(7, 'days').toISOString().substr(0, 10);

    var week_of_year = moment().isoWeek();
    var year = moment().year();
    for(var i=1;i<=52;i++) {
        text = 'Week ' + i;
        value = i;


        if( i == week_of_year) {
            $('#graph-to-week').append(`<option value="${value}" selected> ${text} </option>`); 
        } else {
            $('#graph-to-week').append(`<option value="${value}"> ${text} </option>`); 
        }

        if((week_of_year - 4) < 1) {
            value = 52 - week_of_year;
            text = 'Week ' + value;
        }

        if( i == (week_of_year - 4)) {
            $('#graph-from-week').append(`<option value="${value}" selected> ${text} </option>`); 
        } else {
            $('#graph-from-week').append(`<option value="${value}"> ${text} </option>`); 
        }
    }

    if((week_of_year - 4) < 1) {
        year -= 1;
    }

    $('#graph-from-year').val(year);
    $('#graph-to-year').val(moment().year());

    getGraphData();
    
});

// Utility function to add days to a date
// function addDays(date, days) {
//     const copy = new Date(Number(date))
//     copy.setDate(date.getDate() + days)
//     return copy
// }

// Utility function to find number of days berween two dates
// function daysBetween( date1, date2 ) {
//     //Get 1 day in milliseconds
//     var one_day=1000*60*60*24;

//     // Convert both dates to milliseconds
//     var date1_ms = date1.getTime();
//     var date2_ms = date2.getTime();

//     // Calculate the difference in milliseconds
//     var difference_ms = date2_ms - date1_ms;
        
//     // Convert back to days and return
//     return Math.round(difference_ms/one_day); 
// }

$("#graph-left-jump").click(function(){

    var from_date = new Date($('#graph-from-date').val());
    var to_date = new Date($('#graph-to-date').val());

    var new_from_date = from_date;
    var new_to_date = to_date;

    if(data_summary_type == 'daily') {

        new_from_date.setDate(new_from_date.getDate() - 7);
        new_to_date.setDate(new_to_date.getDate() - 7);

    } else if (data_summary_type == 'weekly') {
        
        var from_week_select = $('#graph-from-week');
        var to_week_select = $('#graph-to-week');

        var from_week = from_week_select.val();
        var to_week = to_week_select.val();

        var new_from_week = parseInt(from_week) - 1;
        var new_to_week = parseInt(to_week) - 1 ;

        if(new_from_week < 1) {
            new_from_week = 52;
            var year = $('#graph-from-year').val();
            $('#graph-from-year').val(parseInt(year)-1);
        }

        if(new_to_week < 1) {
            new_to_week = 52;
            var year = $('#graph-to-year').val();
            $('#graph-to-year').val(parseInt(year)-1);
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
    $("#graph-to-date").val(new_to_date.toISOString().substr(0, 10));4

    getGraphData();
});

$("#graph-right-jump").click(function(){

    var from_date = new Date($('#graph-from-date').val());
    var to_date = new Date($('#graph-to-date').val());

    var new_from_date = from_date;
    var new_to_date = to_date;

    if(data_summary_type == 'daily') {

        new_from_date.setDate(new_from_date.getDate() + 7);
        new_to_date.setDate(new_to_date.getDate() + 7);

    } else if (data_summary_type == 'weekly') {
        
        var from_week_select = $('#graph-from-week');
        var to_week_select = $('#graph-to-week');

        var from_week = from_week_select.val();
        var to_week = to_week_select.val();

        var new_from_week = parseInt(from_week) + 1;
        var new_to_week = parseInt(to_week) + 1 ;

        if(new_from_week > 52) {
            new_from_week = 1;
            var year = $('#graph-from-year').val();
            $('#graph-from-year').val(parseInt(year) +1);
        }

        if(new_to_week > 52) {
            new_to_week = 1;
            var year = $('#graph-to-year').val();
            $('#graph-to-year').val(parseInt(year)+1);
        }

        if(new_to_week > moment().isoWeek()) {
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

    if(new_to_date > moment()) {
        return;
    }

    $("#graph-from-date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph-to-date").val(new_to_date.toISOString().substr(0, 10));

    getGraphData();
});

$("#graph-left-crawl").click(function(){

    var from_date = new Date($('#graph-from-date').val());
    var to_date = new Date($('#graph-to-date').val());

    var new_from_date = from_date;
    var new_to_date = to_date;

    if(data_summary_type == 'daily') {

        new_from_date.setDate(new_from_date.getDate() - 1);
        new_to_date.setDate(new_to_date.getDate() - 1);

    } else if (data_summary_type == 'weekly') {
        
        var from_week_select = $('#graph-from-week');
        var to_week_select = $('#graph-to-week');

        var from_week = from_week_select.val();
        var to_week = to_week_select.val();

        var new_from_week = parseInt(from_week) - 1;
        var new_to_week = parseInt(to_week) - 1 ;

        if(new_from_week < 1) {
            new_from_week = 52;
            var year = $('#graph-from-year').val();
            $('#graph-from-year').val(parseInt(year)-1);
        }

        if(new_to_week < 1) {
            new_to_week = 52;
            var year = $('#graph-to-year').val();
            $('#graph-to-year').val(parseInt(year)-1);
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

    if(new_to_date > moment()) {
        return;
    }

    $("#graph-from-date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph-to-date").val(new_to_date.toISOString().substr(0, 10));

    getGraphData();
});

$("#graph-right-crawl").click(function(){

    var from_date = new Date($('#graph-from-date').val());
    var to_date = new Date($('#graph-to-date').val());

    var new_from_date = from_date;
    var new_to_date = to_date;

    if(data_summary_type == 'daily') {

        new_from_date.setDate(new_from_date.getDate() + 1);
        new_to_date.setDate(new_to_date.getDate() + 1);

    } else if (data_summary_type == 'weekly') {
        
        var from_week_select = $('#graph-from-week');
        var to_week_select = $('#graph-to-week');

        var from_week = from_week_select.val();
        var to_week = to_week_select.val();

        var new_from_week = parseInt(from_week) + 1;
        var new_to_week = parseInt(to_week) + 1 ;

        if(new_from_week > 52) {
            new_from_week = 1;
            var year = $('#graph-from-year').val();
            $('#graph-from-year').val(parseInt(year) +1);
        }

        if(new_to_week > 52) {
            new_to_week = 1;
            var year = $('#graph-to-year').val();
            $('#graph-to-year').val(parseInt(year)+1);
        }

        if(new_to_week > moment().isoWeek()) {
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

    if(new_to_date > moment()) {
        return;
    }

    $("#graph-from-date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph-to-date").val(new_to_date.toISOString().substr(0, 10));

    getGraphData();
});

$("#graph-zoom-out").click(function(){

    var from_date = new Date($('#graph-from-date').val());
    var to_date = new Date($('#graph-to-date').val());

    var new_from_date = from_date;
    var new_to_date = to_date;

    if(data_summary_type == 'daily') {

        new_from_date.setDate(new_from_date.getDate() - 1);
        new_to_date.setDate(new_to_date.getDate() + 1);

        if(new_to_date > moment()) {

            new_from_date.setDate(new_from_date.getDate() - 1);
            new_to_date = moment();

        }

    } else if (data_summary_type == 'weekly') {
        
        var from_week_select = $('#graph-from-week');
        var to_week_select = $('#graph-to-week');

        var from_week = from_week_select.val();
        var to_week = to_week_select.val();

        var new_from_week = parseInt(from_week) - 1;
        var new_to_week = parseInt(to_week) + 1 ;

        if(new_to_week >= moment().isoWeek()) {
            new_to_week = to_week;
            new_from_week -= 1;
        }

        if(new_from_week > 52) {
            new_from_week = 1;
            var year = $('#graph-from-year').val();
            $('#graph-from-year').val(parseInt(year) +1);
        }

        if(new_to_week > 52) {
            new_to_week = 1;
            var year = $('#graph-to-year').val();
            $('#graph-to-year').val(parseInt(year)+1);
        }


        if(new_from_week < 1) {
            new_from_week = 52;
            var year = $('#graph-from-year').val();
            $('#graph-from-year').val(parseInt(year)-1);
        }


        if(new_to_week < 1) {
            new_to_week = 52;
            var year = $('#graph-to-year').val();
            $('#graph-to-year').val(parseInt(year)-1);
        }

        from_week_select.val(new_from_week);
        to_week_select.val(new_to_week);

    } else if (data_summary_type == 'monthly') {

        new_from_date.setMonth(new_from_date.getMonth() - 1);
        new_to_date.setMonth(new_to_date.getMonth() + 1);

        if(new_to_date > moment()) {

            new_from_date.setDate(new_from_date.getMonth() - 1);
            new_to_date = moment();

        }

    } else {

        new_from_date.setFullYear(new_from_date.getFullYear() - 1);
        new_to_date.setFullYear(new_to_date.getFullYear() + 1);

        if(new_to_date > moment()) {

            new_from_date.setFullYear(new_from_date.getFullYear() - 1);
            new_to_date = moment();

        }

    }

    $("#graph-from-date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph-to-date").val(new_to_date.toISOString().substr(0, 10));

    getGraphData();
});

$("#graph-zoom-in").click(function(){

    var from_date = new Date($('#graph-from-date').val());
    var to_date = new Date($('#graph-to-date').val());

    var new_from_date = from_date;
    var new_to_date = to_date;

    if(data_summary_type == 'daily') {

        new_from_date.setDate(new_from_date.getDate() + 1);
        new_to_date.setDate(new_to_date.getDate() - 1);

    } else if (data_summary_type == 'weekly') {
        
        var from_week_select = $('#graph-from-week');
        var to_week_select = $('#graph-to-week');

        var from_week = from_week_select.val();
        var to_week = to_week_select.val();

        var new_from_week = parseInt(from_week) + 1;
        var new_to_week = parseInt(to_week) - 1 ;

        if(new_from_week > 52) {
            new_from_week = 1;
            var year = $('#graph-from-year').val();
            $('#graph-from-year').val(parseInt(year) +1);
        }

        if(new_to_week > 52) {
            new_to_week = 1;
            var year = $('#graph-to-year').val();
            $('#graph-to-year').val(parseInt(year)+1);
        }


        if(new_from_week < 1) {
            new_from_week = 52;
            var year = $('#graph-from-year').val();
            $('#graph-from-year').val(parseInt(year)-1);
        }


        if(new_to_week < 1) {
            new_to_week = 52;
            var year = $('#graph-to-year').val();
            $('#graph-to-year').val(parseInt(year)-1);
        }

        if(new_from_week >= new_to_week && $('#graph-from-year').val() === $('#graph-to-year').val()) {
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

    if(new_from_date >= new_to_date) {
        return;
    }

    $("#graph-from-date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph-to-date").val(new_to_date.toISOString().substr(0, 10));

    getGraphData();
});