// JS for Location Report Page

// Region data table config
var stateReportTable = $('#region-report-table').DataTable({
    scrollX: false,
    columns: [
        { "width": "65%" },
        { "width": "15%" },
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

// City data table config
var cityReportTable = $('#city-report-table').DataTable({
    scrollX: false,
    columns: [
        { "width": "65%" },
        { "width": "15%" },
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
$('#location-select').on('change', function() {
    if ($('#location-select').val() == 'region') {
        $('#region-table').show();
        $('#city-table').hide();
    } else {
        $('#city-table').show();
        $('#region-table').hide();
    }
});