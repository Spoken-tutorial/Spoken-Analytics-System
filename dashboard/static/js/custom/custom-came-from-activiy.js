var cameFromActivityDataTable = $('#came-from-activity-data-table').DataTable({
    searching: false,
    scrollX: false,
    columns: [
        { "width": "10%" },
        { "width": "10%" },
        { "width": "50%" },
        { "width": "30%" },
    ],
    lengthMenu: [
        [10, 25, 50, -1],
        [10, 25, 50, "All"]
    ]
});