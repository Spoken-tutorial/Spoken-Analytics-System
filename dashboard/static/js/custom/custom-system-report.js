// JS for System Report Page

// Browser data table config
var browserReportTable = $('#browser-report-table').DataTable({
    scrollX: false,
    columns: [
        { "width": "35%" },
        { "width": "50%" },
        { "width": "15%" },
    ],
    order: [
        [1, 'desc']
    ],
    lengthMenu: [
        [10, 25, 50, -1],
        [10, 25, 50, "All"]
    ]
});

// Platform data table config
var platformReportTable = $('#platform-report-table').DataTable({
    scrollX: false,
    columns: [
        { "width": "35%" },
        { "width": "50%" },
        { "width": "15%" },
    ],
    order: [
        [1, 'desc']
    ],
    lengthMenu: [
        [10, 25, 50, -1],
        [10, 25, 50, "All"]
    ]
});

// OS data table config
var platformReportTable = $('#os-report-table').DataTable({
    scrollX: false,
    columns: [
        { "width": "35%" },
        { "width": "50%" },
        { "width": "15%" },
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
$('#system-select').on('change', function() {
    if ($('#system-select').val() == "browser") {
        $('#browser-table').show();
        $('#platform-table').hide();
        $('#os-table').hide();
    } else if ($('#system-select').val() == "platform") {
        $('#browser-table').hide();
        $('#platform-table').show();
        $('#os-table').hide();
    } else {
        $('#browser-table').hide();
        $('#platform-table').hide();
        $('#os-table').show();
    }
});