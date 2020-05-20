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