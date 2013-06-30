$(document).ready(function(){
    $("#vid_button").hide();
    $("#movie").hide();


    var timerVid = $.timer(function(){
        $("#movie").slideToggle();
        timerVid.stop();
    });
    timerVid.set({time:3000,autostart:true});

    var timerButton = $.timer(function(){
        $("#vid_button").slideToggle();
        timerButton.stop();
    });
    timerButton.set({time:2500,autostart:true});


    $(function() {
    $("#vid_button")
        .mouseover(function() {
            var src = $(this).attr("src").match(/[^\.]+/) + "_hover.png";
            $(this).attr("src", src);
        })
        .mouseout(function() {
            var src = $(this).attr("src").replace("_hover.png", ".png");
            $(this).attr("src", src);
        });
    });

    $("#vid_button").click(function(){
        $("#movie").slideToggle();
    });
});