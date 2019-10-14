/**
 * Resize function without multiple trigger
 *
 * Usage:
 * $(window).smartresize(function(){
 *     // code here
 * });
 */
(function($, sr) {
    // debouncing function from John Hann
    // http://unscriptable.com/index.php/2009/03/20/debouncing-javascript-methods/
    var debounce = function(func, threshold, execAsap) {
        var timeout;

        return function debounced() {
            var obj = this,
                args = arguments;

            function delayed() {
                if (!execAsap)
                    func.apply(obj, args);
                timeout = null;
            }

            if (timeout)
                clearTimeout(timeout);
            else if (execAsap)
                func.apply(obj, args);

            timeout = setTimeout(delayed, threshold || 100);
        };
    };

    // smartresize
    jQuery.fn[sr] = function(fn) {
        return fn ? this.bind('resize', debounce(fn)) : this.trigger(sr);
    };
})(jQuery, 'smartresize');

/**
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

var CURRENT_URL = window.location.href.split('#')[0].split('?')[0],
    $BODY = $('body'),
    $MENU_TOGGLE = $('#menu_toggle'),
    $SIDEBAR_MENU = $('#sidebar-menu'),
    $SIDEBAR_FOOTER = $('.sidebar-footer'),
    $LEFT_COL = $('.left_col'),
    $RIGHT_COL = $('.right_col'),
    $NAV_MENU = $('.nav_menu'),
    $FOOTER = $('footer');


// Sidebar
function init_sidebar() {
    // TODO: This is some kind of easy fix, maybe we can improve this
    var setContentHeight = function() {
        // reset height
        $RIGHT_COL.css('min-height', $(window).height());

        var bodyHeight = $BODY.outerHeight(),
            footerHeight = $BODY.hasClass('footer_fixed') ? -10 : $FOOTER.height(),
            leftColHeight = $LEFT_COL.eq(1).height() + $SIDEBAR_FOOTER.height(),
            contentHeight = bodyHeight < leftColHeight ? leftColHeight : bodyHeight;

        // normalize content
        contentHeight -= $NAV_MENU.height() + footerHeight;

        $RIGHT_COL.css('min-height', contentHeight);
    };

    $SIDEBAR_MENU.find('a').on('click', function(ev) {
        console.log('clicked - sidebar_menu');
        var $li = $(this).parent();

        if ($li.is('.active')) {
            $li.removeClass('active active-sm');
            $('ul:first', $li).slideUp(function() {
                setContentHeight();
            });
        } else {
            // prevent closing menu if we are on child menu
            if (!$li.parent().is('.child_menu')) {
                $SIDEBAR_MENU.find('li').removeClass('active active-sm');
                $SIDEBAR_MENU.find('li ul').slideUp();
            } else {
                if ($BODY.is(".nav-sm")) {
                    $SIDEBAR_MENU.find("li").removeClass("active active-sm");
                    $SIDEBAR_MENU.find("li ul").slideUp();
                }
            }
            $li.addClass('active');

            $('ul:first', $li).slideDown(function() {
                setContentHeight();
            });
        }
    });

    // toggle small or large menu
    $MENU_TOGGLE.on('click', function() {
        console.log('clicked - menu toggle');

        if ($BODY.hasClass('nav-md')) {
            $SIDEBAR_MENU.find('li.active ul').hide();
            $SIDEBAR_MENU.find('li.active').addClass('active-sm').removeClass('active');
        } else {
            $SIDEBAR_MENU.find('li.active-sm ul').show();
            $SIDEBAR_MENU.find('li.active-sm').addClass('active').removeClass('active-sm');
        }

        $BODY.toggleClass('nav-md nav-sm');

        setContentHeight();
    });

    // check active menu
    $SIDEBAR_MENU.find('a[href="' + CURRENT_URL + '"]').parent('li').addClass('current-page');

    $SIDEBAR_MENU.find('a').filter(function() {
        return this.href == CURRENT_URL;
    }).parent('li').addClass('current-page').parents('ul').slideDown(function() {
        setContentHeight();
    }).parent().addClass('active');

    // recompute content when resizing
    $(window).smartresize(function() {
        setContentHeight();
    });

    setContentHeight();

    // fixed sidebar
    if ($.fn.mCustomScrollbar) {
        $('.menu_fixed').mCustomScrollbar({
            autoHideScrollbar: true,
            theme: 'minimal',
            mouseWheel: { preventDefault: true }
        });
    }
};
// /Sidebar

var randNum = function() {
    return (Math.floor(Math.random() * (1 + 40 - 20))) + 20;
};

// Panel toolbox
$(document).ready(function() {
    $('.collapse-link').on('click', function() {
        var $BOX_PANEL = $(this).closest('.x_panel'),
            $ICON = $(this).find('i'),
            $BOX_CONTENT = $BOX_PANEL.find('.x_content');

        // fix for some div with hardcoded fix class
        if ($BOX_PANEL.attr('style')) {
            $BOX_CONTENT.slideToggle(200, function() {
                $BOX_PANEL.removeAttr('style');
            });
        } else {
            $BOX_CONTENT.slideToggle(200);
            $BOX_PANEL.css('height', 'auto');
        }

        $ICON.toggleClass('fa-chevron-up fa-chevron-down');
    });

    $('.close-link').click(function() {
        var $BOX_PANEL = $(this).closest('.x_panel');

        $BOX_PANEL.remove();
    });
});
// /Panel toolbox



// Progressbar
if ($(".progress .progress-bar")[0]) {
    $('.progress .progress-bar').progressbar();
}
// /Progressbar

function init_chart_doughnut() {

    console.log('----------1------------');
    /*
    $.ajax({
        url:'/socialanalyzer/recent_search_twitter/recent_search',
        type: 'GET',success: function showAnswer(data) {
            //console.log("-------success 1-------",data);
            if (data.code==200) {
                console.log("-------success-------",data);
                var delayInMilliseconds = 2000; // 2 second
                setTimeout(function() {
                    location.reload(true);
                }, delayInMilliseconds);
            }else{
                console.log('Error, status:',data.code);
            }
        }
    })
    */
    if (typeof(Chart) === 'undefined') {
        return;
    }

    console.log('init_chart_doughnut');

    if ($('.recently_search').length) {

        var chart_doughnut_settings = {
            type: 'doughnut',
            tooltipFillColor: "rgba(51, 51, 51, 0.55)",
            data: {
                labels: [
                    "Positivas",
                    "Negativas",
                    "Neutrales"
                ],
                datasets: [{
                    data: [45, 35, 20],
                    backgroundColor: [
                        "#26B99A",
                        "#E74C3C",
                        "#BDC3C7"
                    ],
                    hoverBackgroundColor: [
                        "#36CAAB",
                        "#E95E4F",
                        "#CFD4D8"
                    ]
                }]
            },
            options: {
                legend: false,
                responsive: false
            }
        }

        $('.recently_search').each(function() {

            var chart_element = $(this);
            var chart_doughnut = new Chart(chart_element, chart_doughnut_settings);

        });

    }

    if ($('.top_positive_search').length) {

        var chart_doughnut_settings = {
            type: 'doughnut',
            tooltipFillColor: "rgba(51, 51, 51, 0.55)",
            data: {
                labels: [
                    "Positivas",
                    "Negativas",
                    "Neutrales"
                ],
                datasets: [{
                    data: [45, 35, 20],
                    backgroundColor: [
                        "#26B99A",
                        "#E74C3C",
                        "#BDC3C7"
                    ],
                    hoverBackgroundColor: [
                        "#36CAAB",
                        "#E95E4F",
                        "#CFD4D8"
                    ]
                }]
            },
            options: {
                legend: false,
                responsive: false
            }
        }

        $('.top_positive_search').each(function() {

            var chart_element = $(this);
            var chart_doughnut = new Chart(chart_element, chart_doughnut_settings);

        });

    }

    if ($('.top_negative_search').length) {

        var chart_doughnut_settings = {
            type: 'doughnut',
            tooltipFillColor: "rgba(51, 51, 51, 0.55)",
            data: {
                labels: [
                    "Positivas",
                    "Negativas",
                    "Neutrales"
                ],
                datasets: [{
                    data: [45, 35, 20],
                    backgroundColor: [
                        "#26B99A",
                        "#E74C3C",
                        "#BDC3C7"
                    ],
                    hoverBackgroundColor: [
                        "#36CAAB",
                        "#E95E4F",
                        "#CFD4D8"
                    ]
                }]
            },
            options: {
                legend: false,
                responsive: false
            }
        }

        $('.top_negative_search').each(function() {

            var chart_element = $(this);
            var chart_doughnut = new Chart(chart_element, chart_doughnut_settings);

        });

    }    
}


function wordSearchedDetail(word){
    //console.log("-------wordSearchedDetail-------",word)
    $.ajax({
        url:'/socialanalyzer/timeline_search_twitter/',
        type: 'GET',
        data: {
          'word': word,
     },success: function showAnswer(data) {
        console.log("-------DATA-------",data.code)
        window.location.href = "web/word_searched_details_twitter.html";
        if (data.code==200) {

            console.log("-------data-------",data)

        }else{
            console.log('Error to load modal');
          }
        }
    })
}

$(document).ready(function() {
/*
    init_sparklines();
    init_flot_chart();
*/
    init_sidebar();
/*
    init_wysiwyg();
    init_InputMask();
    init_JQVmap();
    init_cropper();
    init_knob();
    init_IonRangeSlider();
    init_ColorPicker();
    init_TagsInput();
*/
    //init_parsley();
/*
    init_daterangepicker();
    init_daterangepicker_right();
    init_daterangepicker_single_call();
    init_daterangepicker_reservation();
    init_SmartWizard();
    init_EasyPieChart();
    init_charts();
    init_echarts();
    init_morris_charts();
    init_skycons();
    init_select2();
    init_validator();
    init_DataTables();
*/    
    init_chart_doughnut();
/*
    init_gauge();
    init_PNotify();
    init_starrr();
    init_calendar();
    init_compose();
    init_CustomNotification();
    init_autosize();
    init_autocomplete();
*/
});
