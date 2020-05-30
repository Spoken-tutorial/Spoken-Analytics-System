// JS for visitor path page

var visitorPathDataTable = $('#visitor-path-data-table').DataTable({
    searching: true,
    scrollX: false,
    columns: [
        { "width": "100%" },
    ],
    lengthMenu: [
        [10, 25, 50, -1],
        [10, 25, 50, "All"]
    ]
});

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
        url: "/dashboard/visitor_path_data/",
        success: function(data) {

            // Parsing the data
            data = JSON.parse(data);
            console.log(data);

            data_table_array = []

            // Inserting data to data_table_array
            data.forEach((key, value) => {
                var path = ''
                for (element of JSON.parse(key.fields.path)) {
                    path += '<div class="row"><div class="col-md-4"></div><div class="col-md-8"><a href="' + element.referrer + '" style="text-decoration: none; color: green">' + element.referrer + '</a></div></div><div class="row"><div class="col-md-2">' + moment(element.datetime).format('YYYY-MM-DD') + '</div><div class="col-md-2">' + moment(element.datetime).format('HH:mm') + '</div><div class="col-md-8">' + element.page_url + '</div></div><br>'
                }
                data_table_array.push([
                    '<td><div class="row info-row"><div class="col-md-6 no-padding">' + key.fields.city + ', ' + key.fields.region + ', ' + key.fields.country + '&nbsp <span style="font-weight: 700;">' + key.fields.ip_address + '</span></div><div class="col-md-1 no-padding">visit #' + key.fields.visit_num + '</div><div class="col-md-5 no-padding">' + key.fields.os + ', ' + key.fields.browser + ', ' + key.fields.device + '</div></div><div class="paths">' + path + '</div></td>'
                ])
            });

            console.log(data_table_array);

            // Clearing the DataTable and adding rows with new data
            visitorPathDataTable.clear().rows.add(data_table_array).draw();
        },
        error: function(err) {
            console.log("Error:" + err);
        }
    });
}

$(function() {
    getData();
});