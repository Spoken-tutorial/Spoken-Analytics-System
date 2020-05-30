// JS for exit link activity page

var exitLinkActivityDataTable = $('#exit-link-activity-data-table').DataTable({
    searching: false,
    scrollX: false,
    columns: [
        { "width": "10%" },
        { "width": "10%" },
        { "width": "40%" },
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
        url: "/dashboard/exit_link_activity_data/",
        success: function(data) {

            // Parsing the data
            data = JSON.parse(data);

            data_table_array = []

            // Inserting data to data_table_array
            data.forEach((key, value) => {
                data_table_array.push([
                    '<td>' + moment(key.fields.datetime).format('YYYY-MM-DD') + '</td>',
                    '<td>' + moment(key.fields.datetime).format('HH:mm') + '</td>',
                    '<td><a href="' + key.fields.exit_link_clicked + '" style="text-decoration: none; color: blue">' + key.fields.exit_link_clicked + '</a></td>',
                    '<td><a href="https://spoken-tutorial.org' + key.fields.exit_link_page + '">https://spoken-tutorial.org' + key.fields.exit_link_page + '</a></td>'
                ])
            });

            // Clearing the DataTable and adding rows with new data
            exitLinkActivityDataTable.clear().rows.add(data_table_array).draw();
        },
        error: function(err) {
            console.log("Error:" + err);
        }
    });
}

$(function() {
    getData();
});