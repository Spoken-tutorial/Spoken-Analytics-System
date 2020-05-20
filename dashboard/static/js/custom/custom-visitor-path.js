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