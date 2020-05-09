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