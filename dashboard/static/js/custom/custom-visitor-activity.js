// JS for visitor activity page

var visitorActivityDataTable = $('#visitor-activity-data-table').DataTable({
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