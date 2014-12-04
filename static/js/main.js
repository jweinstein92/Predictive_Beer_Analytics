$(document).ready(function () {

    //var $box = $('#colorPicker');
    //    $box.tinycolorpicker();
    //    var box = $box.data("plugin_tinycolorpicker")
    //
    //    box.setColor("#ff0000");
    //var $box = $('.colorbox');
    //    $($($box).children()[0]).addClass("selected");

    $(document).ajaxStart(function () {
        $(".js-loading").show();
    }).ajaxStop(function () {
        $(".js-loading").hide();
    });

    $(document).on('submit', "#prediction-form", function (e) {
        e.preventDefault();

            var form = $(this);
            console.log(document.forms);

            $.ajax({
                type: 'POST',
                data: form.serialize(),
                url: form.attr('action'),
                success: function(data) {
                    $('#prediction-result').html(data);
                }
            });
    });

    $(document).on('click', "#desc-query-btn", function (e) {
        e.preventDefault();

            var form = $("#desc-query-form");
            $.ajax({
                type: 'POST',
                data: form.serialize(),
                url: form.attr('action'),
                success: function(data) {
                    $('#desc-result').inner(data);

                }
            });
    });


});
