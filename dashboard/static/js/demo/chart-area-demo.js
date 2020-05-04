var timeFormat = 'YYYY-MM-DD';

daily_page_loads_array = []
daily_unique_visits_array = []
daily_returning_visits_array = []

var color = Chart.helpers.color; // chart.js colors

var ctx_day_chart = document.getElementById("myAreaChart").getContext('2d');

// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

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
        backgroundColor: color('rgb(78,115,223)').alpha(0.5).rgbString(),
        borderColor: 'rgb(78,115,223)',
        fill: false,
        data: daily_page_loads_array,
      },{
        label: 'Unique Visits',
        backgroundColor: color('rgb(28,200,138)').alpha(0.5).rgbString(),
        borderColor: 'rgb(28,200,138)',
        fill: false,
        data: daily_unique_visits_array,
      },{
        label: 'Returning Visits',
        backgroundColor: color('rgb(246,194,62)').alpha(0.5).rgbString(),
        borderColor: 'rgb(246,194,62)',
        fill: false,
        data: daily_returning_visits_array,
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
                  tooltipFormat: 'll'
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
              }
          }],
          yAxes: [{
            ticks: {
              maxTicksLimit: 5,
              padding: 10,
              // Include a dollar sign in the ticks
              callback: function(value, index, values) {
                  return number_format(value);
                }
              },
              display: true,
              scaleLabel: {
                  display: true,
                  labelString: 'Views'
              },
          }]
      }
  }
};

function getGraphData(){
    // Getting chart data from server 
    fromDate = $('#graph_from_date').val()
    toDate = $('#graph_to_date').val()

    $.ajax({
    type: "GET",
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    data: {
        fromDate: fromDate,
        toDate: toDate,
    },
    url: "/dashboard/graph_data/",
    success: function(data) {

        daily_page_loads_array.length = 0
        daily_unique_visits_array.length = 0
        daily_returning_visits_array.length = 0

        daily_page_loads = JSON.parse(data.daily_page_loads_json);
        daily_unique_visits = JSON.parse(data.daily_unique_visits_json)
        daily_returning_visits = JSON.parse(data.daily_returning_visits_json)

        daily_page_loads.forEach((key, value) => {
            // pushing chart data in daily_page_loads_array variable
            daily_page_loads_array.push({
                'x': moment(key._id.date).format(timeFormat),
                'y': key.count,
            })
        });

        daily_unique_visits.forEach((key, value) => {
            // pushing chart data in daily_unique_visits variable
            daily_unique_visits_array.push({
                'x': moment(key._id.date).format(timeFormat),
                'y': key.count,
            })
        });

        daily_returning_visits.forEach((key, value) => {
            // pushing chart data in daily_unique_visits variable
            daily_returning_visits_array.push({
                'x': moment(key._id.date).format(timeFormat),
                'y': key.count,
            })
        });

        new Chart(ctx_day_chart, config);
    },
    error: function(err) {
        console.log("Error:" + err);
    }
    });
}

$('#chart_select').on('change', function() {
    config.type = $('#chart_select').val();
    getGraphData();
});

$(document).ready( function () {
    document.querySelector("#graph_to_date").value = moment().toISOString().substr(0, 10);
    document.querySelector("#graph_from_date").value = moment().subtract(7, 'days').toISOString().substr(0, 10);
    getGraphData();
});

// Utility function to add days to a date
function addDays(date, days) {
    const copy = new Date(Number(date))
    copy.setDate(date.getDate() + days)
    return copy
}

// Utility function to find number of days berween two dates
function daysBetween( date1, date2 ) {
    //Get 1 day in milliseconds
    var one_day=1000*60*60*24;

    // Convert both dates to milliseconds
    var date1_ms = date1.getTime();
    var date2_ms = date2.getTime();

    // Calculate the difference in milliseconds
    var difference_ms = date2_ms - date1_ms;
        
    // Convert back to days and return
    return Math.round(difference_ms/one_day); 
}

$("#graph-left-jump").click(function(){
    var from_date = new Date($('#graph_from_date').val());
    var to_date = new Date($('#graph_to_date').val());
    var new_from_date = addDays(from_date, -7);
    var new_to_date = addDays(to_date, -7);
    $("#graph_from_date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph_to_date").val(new_to_date.toISOString().substr(0, 10));
    getGraphData();
});

$("#graph-right-jump").click(function(){
    var from_date = new Date($('#graph_from_date').val());
    var to_date = new Date($('#graph_to_date').val());
    var today = new Date();
    var new_from_date = addDays(from_date, 7);
    var new_to_date = addDays(to_date, 7);
    var diff_days = daysBetween(new_to_date, today);
    if(diff_days == -7) {
        return;
    } else if(diff_days >= -7) {
        $("#graph_from_date").val(addDays(from_date, 7+diff_days).toISOString().substr(0, 10));
        $("#graph_to_date").val(addDays(to_date, 7+diff_days).toISOString().substr(0, 10));
        getGraphData();
    } else {
        $("#graph_from_date").val(new_from_date.toISOString().substr(0, 10));
        $("#graph_to_date").val(new_to_date.toISOString().substr(0, 10));
        getGraphData();
    }
});

$("#graph-left-crawl").click(function(){
    var from_date = new Date($('#graph_from_date').val());
    var to_date = new Date($('#graph_to_date').val());
    var new_from_date = addDays(from_date, -1);
    var new_to_date = addDays(to_date, -1);
    $("#graph_from_date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph_to_date").val(new_to_date.toISOString().substr(0, 10));
    getGraphData();
});

$("#graph-right-crawl").click(function(){
    var from_date = new Date($('#graph_from_date').val());
    var to_date = new Date($('#graph_to_date').val());
    var today = new Date();
    var new_from_date = addDays(from_date, 1);
    var new_to_date = addDays(to_date, 1);
    if(daysBetween(new_to_date, today) < 0) {
        return;
    }
    $("#graph_from_date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph_to_date").val(new_to_date.toISOString().substr(0, 10));
    getGraphData();
});

$("#graph-zoom-out").click(function(){
    var from_date = new Date($('#graph_from_date').val());
    var to_date = new Date($('#graph_to_date').val());
    var today = new Date();
    var new_from_date = addDays(from_date, -1);
    var new_to_date = addDays(to_date, 1);
    if(daysBetween(today, new_to_date) > 0) {
        $("#graph_from_date").val(addDays(from_date, -2).toISOString().substr(0, 10));
    } else {
        $("#graph_from_date").val(new_from_date.toISOString().substr(0, 10));
        $("#graph_to_date").val(new_to_date.toISOString().substr(0, 10));
    }
    getGraphData();
});

$("#graph-zoom-in").click(function(){
    var from_date = new Date($('#graph_from_date').val());
    var to_date = new Date($('#graph_to_date').val());
    var new_from_date = addDays(from_date, 1);
    var new_to_date = addDays(to_date, -1);
    if(daysBetween(from_date, to_date) < 4) {
        return;
    }
    $("#graph_from_date").val(new_from_date.toISOString().substr(0, 10));
    $("#graph_to_date").val(new_to_date.toISOString().substr(0, 10));
    getGraphData();
});