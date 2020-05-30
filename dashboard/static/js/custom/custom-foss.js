// JS for Foss Page

// Array to store data of data table
var data_table_array = []

// Data table config
var fossDataTable = $('#foss-data-table').DataTable({
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

    $('#foss-from-date').val(moment().subtract(1, 'days').toISOString().substr(0, 10));
    $('#foss-to-date').val(moment().subtract(1, 'days').toISOString().substr(0, 10));

    getFossData();

});

// Getting table data from server
function getFossData() {

    fromDate = $('#foss-from-date').val();
    toDate = $('#foss-to-date').val();

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
        url: "/dashboard/foss_data/",
        success: function(data) {

            // Parsing the data
            data = JSON.parse(data);

            data_table_array = []

            // Inserting data to data_table_array
            data.forEach((key, value) => {
                data_table_array.push([
                    key.foss_name,
                    key.unique_visits
                ]);
            });

            // Clearing the DataTable and adding rows with new data
            fossDataTable.clear().rows.add(data_table_array).draw();
        },
        error: function(err) {
            console.log("Error:" + err);
        }
    });
}