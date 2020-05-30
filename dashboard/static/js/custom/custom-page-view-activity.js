// JS for page view activity page

var pageViewActivityDataTable = $('#page-view-activity-data-table').DataTable({
    searching: true,
    scrollX: false,
    columns: [
        { "width": "10%" },
        { "width": "10%" },
        { "width": "20%" },
        { "width": "20%" },
        { "width": "40%" },
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
        url: "/dashboard/page_view_activity_data/",
        success: function(data) {

            // Parsing the data
            data = JSON.parse(data);
            console.log(data);

            data_table_array = []

            // Inserting data to data_table_array
            data.forEach((key, value) => {
                data_table_array.push([
                    '<td>' + moment(key.fields.datetime).format('YYYY-MM-DD') + '</td>',
                    '<td>' + moment(key.fields.datetime).format('HH:mm') + '</td>',
                    '<td>' + key.fields.browser + '<br>' + key.fields.os + '<br>' + key.fields.device + '</td>',
                    '<td>' + key.fields.city + ', <br>' + key.fields.region + ',<br>' + key.fields.country + '</td>',
                    '<td>' + key.fields.ip_address + '<br> <a href="https://spoken-tutorial.org' + key.fields.page_url + '" style="text-decoration: none; color: blue">https://spoken-tutorial.org' + key.fields.page_url + '</a><br> <a href="' + key.fields.referrer + '" style="text-decoration: none; color: green">' + key.fields.referrer + '</a></td>'
                ])
            });

            console.log(data_table_array);

            // Clearing the DataTable and adding rows with new data
            pageViewActivityDataTable.clear().rows.add(data_table_array).draw();
        },
        error: function(err) {
            console.log("Error:" + err);
        }
    });
}

$(function() {
    getData();
});