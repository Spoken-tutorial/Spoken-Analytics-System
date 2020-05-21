// JS for keyword activity page

var keywordActivityDataTable = $('#keyword-activity-data-table').DataTable({
    searching: false,
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