//portfolio
$(document).ready(function() {
    var $container = $('#posts').isotope({
        itemSelector: '.item',
        isFitWidth: true
    });

    $(window).smartresize(function() {
        $container.isotope({
            columnWidth: '.col-sm-6'
        });
    });

    $container.isotope({
        filter: '*'
    });

    // filter items on button click
    $('#filters').on('click', 'button', function() {
        var filterValue = $(this).attr('data-filter');
        $container.isotope({
            filter: filterValue
        });
    });

    //active filter check
    $(".button_bg").click(function() {
        $(".button_bg").removeClass("active_port");
        $(this).addClass("active_port");
    });

});