var timeFormat = 'YYYY-MM-DD';

graphData = []

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
  type: 'line',
  data: {
      datasets: [{
          label: 'Page Views',
          backgroundColor: color('rgb(54, 162, 235)').alpha(0.5).rgbString(),
          borderColor: 'rgb(54, 162, 235)',
          fill: false,
          data: graphData,
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
        graphData.length = 0
        data = JSON.parse(data);
        data.forEach((key, value) => {
            // pushing chart data in graphData variable
            graphData.push({
                'x': moment(key._id.date).format(timeFormat),//key._id.date.format(),
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

document.querySelector("#graph_to_date").value = moment().toISOString().substr(0, 10);
document.querySelector("#graph_from_date").value = moment().subtract(7, 'days').toISOString().substr(0, 10);


$(document).ready( function () {
    getGraphData();
});

// Area Chart Example
// var config = {
//   type: 'line',
//   data: {
//     labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
//     datasets: [{
//       label: "Earnings",
//       lineTension: 0.3,
//       backgroundColor: "rgba(78, 115, 223, 0.05)",
//       borderColor: "rgba(78, 115, 223, 1)",
//       pointRadius: 3,
//       pointBackgroundColor: "rgba(78, 115, 223, 1)",
//       pointBorderColor: "rgba(78, 115, 223, 1)",
//       pointHoverRadius: 3,
//       pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
//       pointHoverBorderColor: "rgba(78, 115, 223, 1)",
//       pointHitRadius: 10,
//       pointBorderWidth: 2,
//       data: graphData,
//     }],
//   },
//   options: {
//     maintainAspectRatio: false,
//     layout: {
//       padding: {
//         left: 10,
//         right: 25,
//         top: 25,
//         bottom: 0
//       }
//     },
//     scales: {
//       xAxes: [{
//         type: 'time',
//         time: {
//             parser: timeFormat,
//             unit: 'day',
//             tooltipFormat: 'll'
//         },
//         gridLines: {
//           display: false,
//           drawBorder: false
//         },
//         ticks: {
//           maxTicksLimit: 7
//         }
//       }],
//       yAxes: [{
//         ticks: {
//           maxTicksLimit: 5,
//           padding: 10,
//           // Include a dollar sign in the ticks
//           callback: function(value, index, values) {
//             return '$' + number_format(value);
//           }
//         },
//         gridLines: {
//           color: "rgb(234, 236, 244)",
//           zeroLineColor: "rgb(234, 236, 244)",
//           drawBorder: false,
//           borderDash: [2],
//           zeroLineBorderDash: [2]
//         }
//       }],
//     },
//     legend: {
//       display: false
//     },
//     tooltips: {
//       backgroundColor: "rgb(255,255,255)",
//       bodyFontColor: "#858796",
//       titleMarginBottom: 10,
//       titleFontColor: '#6e707e',
//       titleFontSize: 14,
//       borderColor: '#dddfeb',
//       borderWidth: 1,
//       xPadding: 15,
//       yPadding: 15,
//       displayColors: false,
//       intersect: false,
//       mode: 'index',
//       caretPadding: 10,
//       callbacks: {
//         label: function(tooltipItem, chart) {
//           var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
//           return datasetLabel + ': $' + number_format(tooltipItem.yLabel);
//         }
//       }
//     }
//   }
// };