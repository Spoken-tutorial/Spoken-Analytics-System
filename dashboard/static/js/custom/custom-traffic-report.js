// JS for Traffic Report Page

// Came From data table config
var cameFromReportTable = $('#came-from-report-table').DataTable({
    scrollX: false,
    columns: [
        { "width": "80%" },
        { "width": "20%" },
    ],
    order: [
        [1, 'desc']
    ],
    lengthMenu: [
        [10, 25, 50, -1],
        [10, 25, 50, "All"]
    ]
});

// Event data table config
var exitLinkReportTable = $('#exit-link-report-table').DataTable({
    scrollX: false,
    columns: [
        { "width": "80%" },
        { "width": "20%" },
    ],
    order: [
        [1, 'desc']
    ],
    lengthMenu: [
        [10, 25, 50, -1],
        [10, 25, 50, "All"]
    ]
});

// Toggle display of region or city stats tables
$('#type-select').on('change', function() {
    if ($('#type-select').val() == "came_from") {
        $('#came-from-table').show();
        $('#exit-link-table').hide();
    } else {
        $('#came-from-table').hide();
        $('#exit-link-table').show();
    }
});