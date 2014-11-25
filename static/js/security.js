$(document).ready(function () {
    $("input#submit").click(function(){
        $.ajax({
            type: "POST",
            url: "process.php", //process to mail
            data: $('form.contact').serialize(),
            success: function(msg){
                $("#thanks").html(msg) //hide button and show thank you
                $("#form-content").modal('hide'); //hide popup
            },
            error: function(){
                alert("failure");
            }
        });
    });
});

$(document).on('click', ".js-add-rule", function (e) {
            e.preventDefault();
            alert("hejhej");
})



