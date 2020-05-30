// JS for visitor key.fields page

var visitoractivityDataTable = $('#visitor-activity-data-table').DataTable({
    searching: true,
    scrollX: false,
    columns: [
        { "width": "35%" },
        { "width": "65%" },
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
        url: "/dashboard/visitor_activity_data/",
        success: function(data) {

            // Parsing the data
            data = JSON.parse(data);

            data_table_array = []

            // Inserting data to data_table_array
            data.forEach((key, value) => {
                if (key.fields.page_views == 1) {
                    var visit_latest_page = '<dt>Visit Page:</dt>'
                } else {
                    var visit_latest_page = '<dt>Latest Page:</dt>'
                }
                data_table_array.push([
                    '<td><dl><dt>Page Views:</dt><dd>' + key.fields.page_views + '</dd><dt>Latest Page View:</dt><dd>' + moment(key.fields.latest_page_view).format('YYYY-MM-DD HH:mm') + '</dd><dt>Visit Length:</dt><dd>' + parseInt(key.fields.visit_length_sec / 60) + ' min ' + key.fields.visit_length_sec % 60 + ' sec</dd><dt>System:</dt><dd>' + key.fields.browser + '<br>' + key.fields.os + '<br>' + key.fields.device + '</dd></dl></td>',
                    '<td><dl><dt> Total Visits:</dt><dd>' + key.fields.total_visits + '</dd><dt>Location:</dt><dd>' + key.fields.city + ', ' + key.fields.region + ', ' + key.fields.country + '</dd><dt>IP Address:</dt><dd>' + key.fields.ip_address + '</dd><dt>Referring URL:</dt><dd><a href="' + key.fields.referrer + '" style="text-decoration: none; color: green">' + key.fields.referrer + '</a></dd><dt>Entry Page:</dt><dd><a href="' + key.fields.entry_page + '" style="text-decoration: none; color: blue">' + key.fields.entry_page + '</a></dd>' + visit_latest_page + '<dd><a href="' + key.fields.latest_page + '" style="text-decoration: none; color: blue">' + key.fields.latest_page + '</a></dd></dl></td >'
                ])
            });

            console.log(data_table_array);

            // Clearing the DataTable and adding rows with new data
            visitoractivityDataTable.clear().rows.add(data_table_array).draw();
        },
        error: function(err) {
            console.log("Error:" + err);
        }
    });
}

$(function() {
    getData();
});