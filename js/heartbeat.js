name = "76561197990677771"
room = "1"
data = "name=" + name + "&room=" + room;
$(document).ready(function(){
    $("p").click(function(){
        $.ajax({
            type: "POST",
            url: "/heartbeat",
            data: data
        });
    });
});