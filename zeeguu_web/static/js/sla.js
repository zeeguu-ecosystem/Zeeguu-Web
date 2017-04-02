function showStar(starred)
{
    if (starred) {
        $("#star").html('<i style="color:gold" class="icon-star"></i>');
    } else {
        $("#star").html('<i style="color:lightgray" class="icon-star-empty"></i>');
    }
}


$(function() {
    if (typeof chrome !== "undefined" && !chrome.app.isInstalled) {
        $("#install-extension").click(function() {
            chrome.webstore.install();
        });
    } else {
        $("#install-extension").prop("disabled", true).addClass("disabled");
    }

    $('input').focus(function() {
        $(this).popover('show');
    });


    $('input').blur(function() {
        $(this).popover('hide');
    });

    $("#login").validate({
        rules: {
            email: {
                required: true,
                email: true
            },
            password: {
                required:true,
                minlength: 4
            }
        },

        errorClass: "help-inline",
        errorElement: "span",
        highlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('success');
            $(element).parents('.control-group').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('error');
            $(element).parents('.control-group').addClass('success');
        }
    });

    $("#login input[type=submit]").click(function() {
        return $("form").valid();
    });


    $("#create_account").validate({
        rules: {
            email: {
                required: true,
                email: true
            },
            password: {
                required:true,
                minlength: 4
            },
            name: {
                required: true
            }
        },

        errorClass: "help-inline",
        errorElement: "span",
        highlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('success');
            $(element).parents('.control-group').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('error');
            $(element).parents('.control-group').addClass('success');
        }
    });

    $("#create_account input[type=submit]").click(function() {
        return $("form").valid();
    });

});


function deleteBookmark(id) {
    console.log("deleting " + id);
    $.post("/delete_bookmark/"+id);
    $("#bookmark"+id).fadeOut();
    return false;
}

function unstarBookmark(id, user_id) {
    console.log("unstarring " + id)
    $.post("/unstarred_word/" + id+"/"+user_id);
    $("#star"+id).html('<a href="javascript:void(0);" onclick="starBookmark('+id+','+user_id+')"><i style="color:lightgray" class="icon-star-empty"></i></a>');
}

function starBookmark(id,user_id) {
    console.log("starring " + id)
    $.post("/starred_word/" + id+"/"+user_id);
    $("#star"+id).html('<a href="javascript:void(0);" onclick="unstarBookmark('+id+','+user_id+')"><i style="color:gold" class="icon-star"></i></a>');
}




