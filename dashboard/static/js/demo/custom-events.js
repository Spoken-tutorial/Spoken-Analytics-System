var pagesDataTable = $('#pages-data-table').DataTable({
    searching: false,
    scrollX: false,
    // data: [],
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

$(document).ready(function() {
    $('#event-from-date').val(moment().subtract(1, 'days').toISOString().substr(0, 10));
    $('#event-to-date').val(moment().toISOString().substr(0, 10));
});