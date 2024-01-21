//https://codepen.io/lfrichter/pen/mQJJyB

// Collapse/Expand icon
button = $('#collapse-icon')
button.addClass('fa-xmark');

// Collapse click
$('[data-toggle=sidebar-collapse]').click(function() {
    SidebarCollapse();
});

function SidebarCollapse () {
    $('.sidebar-separator-title').toggleClass('invisible');
    $('.menu-collapsed').toggleClass('d-none');
    $('#wrapper').toggleClass('sidebar-expanded sidebar-collapsed');
    $('#sidebar-wrapper').toggleClass('sidebar-expanded sidebar-collapsed');
    $('#page-content-wrapper').toggleClass('sidebar-expanded sidebar-collapsed');
    $('.sidebar-item').toggleClass('justify-content-start justify-content-center')
    
    // Collapse/Expand icon
    button.toggleClass('fa-xmark fa-bars');
}
