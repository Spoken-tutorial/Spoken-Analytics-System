// JS for Foss Event Report Page

// Foss data table config
var fossReportTable = $('#foss-report-table').DataTable({
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
var eventReportTable = $('#event-report-table').DataTable({
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
$('#foss-event-select').on('change', function() {
    if ($('#foss-event-select').val() == "foss") {
        $('#foss-table').show();
        $('#event-table').hide();
    } else {
        $('#foss-table').hide();
        $('#event-table').show();
    }
});