// JS for Event Analysis Page

// Array to store data of data table
var data_table_array = []

// Data table config
var eventsDataTable = $('#events-data-table').DataTable({
    searching: false,
    scrollX: false,
    columns: [
        { "width": "75%" },
        { "width": "25%" },
    ],
    order: [
        [1, 'desc']
    ],
    lengthMenu: [
        [10, 25, 50, -1],
        [10, 25, 50, "All"]
    ]
});

// Initialization of date selects
$(document).ready(function() {

    $('#event-from-date').val(moment().subtract(1, 'days').toISOString().substr(0, 10));
    $('#event-to-date').val(moment().toISOString().substr(0, 10));

});

// Getting chart data from server
function getEventsData() {

    fromDate = $('#event-from-date').val();
    toDate = $('#event-to-date').val();

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
                    '<span class="text-primary text-uppercase">' + key.event_name + '</span>' + '<br>' + key.path_info,
                    key.unique_visits + '<br><a class="text-primary link" href="/dashboard/event_analysis/' + key.event_name + '"><i class="fa fa-cogs"></i>&nbspPage Analysis</a>',
                ])
            });

            // Clearing the DataTable and adding rows with new data
            eventsDataTable.clear().rows.add(data_table_array).draw();
        },
        error: function(err) {
            console.log("Error:" + err);
        }
    });
}