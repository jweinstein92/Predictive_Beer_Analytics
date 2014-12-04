$(document).ready(function () {

    //var $box = $('#colorPicker');
    //    $box.tinycolorpicker();
    //    var box = $box.data("plugin_tinycolorpicker")
    //
    //    box.setColor("#ff0000");
    //var $box = $('.colorbox');
    //    $($($box).children()[0]).addClass("selected");

    $(document).ajaxStart(function () {
        $(".loading").attr("style", "display:table-cell");
    }).ajaxStop(function () {
        $(".loading").attr("style", "display:none");
    });

    $(document).on('submit', "#prediction-form", function (e) {
        e.preventDefault();

            var form = $(this);
            var formData = form.serialize();
            var colorRating = $('.colorbox .selected').attr('data-role');
            formData += "&colorRating=" + colorRating;

            $('#prediction-result').empty();

            $.ajax({
                type: 'POST',
                data: formData,
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
                    $('#desc-result').html(data);

                }
            });
    });


});
