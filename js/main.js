
var class_ids = "";

removeSpecialChar = function(value){
    return value.replace(/[^a-z0-9\s!^"'@#$%*?.,:;/+/-]/gi, '');
}

timeout = function() {
    var t = setTimeout("timeoutPopup();", 39600000);
}

timeoutPopup = function() {
    alert('Warning: This session has been active for 11 hours and will timeout in 1 hour. Please re-login to renew your token.');
}

append_class = function(ident){//--------------------------------------------------appends a class to the list
    if (class_ids == "")
        class_ids = ident;
    else
        class_ids = class_ids + ", " + ident;
}

translate_classes = function(classes){//-----------------------------------------translates classes in to id's
    class_ids = ""
    if (classes[9] == '1') {
        if (classes[0] == '1')
            append_class('#scout_red');
        if (classes[1] == '1')
            append_class('#soldier_red');
        if (classes[2] == '1')
            append_class('#pyro_red');
        if (classes[3] == '1')
            append_class('#demo_red');
        if (classes[4] == '1')
            append_class('#heavy_red');
        if (classes[5] == '1')
            append_class('#medic_red');
        if (classes[6] == '1')
            append_class('#engie_red');
        if (classes[7] == '1')
            append_class('#sniper_red');
        if (classes[8] == '1')
            append_class('#spy_red');
    }else{
        if (classes[0] == '1')
            append_class('#scout');
        if (classes[1] == '1')
            append_class('#soldier');
        if (classes[2] == '1')
            append_class('#pyro');
        if (classes[3] == '1')
            append_class('#demo');
        if (classes[4] == '1')
            append_class('#heavy');
        if (classes[5] == '1')
            append_class('#medic');
        if (classes[6] == '1')
            append_class('#engie');
        if (classes[7] == '1')
            append_class('#sniper');
        if (classes[8] == '1')
            append_class('#spy');
    }
}

sendMessage = function(path, opt_param){//--------------------------------------
    if (opt_param) {
        path += '?' + opt_param;
    }
    var xhr = new XMLHttpRequest();
    xhr.open('POST', path, true);
    xhr.send();
}

openChannel = function(){//-----------------------------------------------------
    var channel = new goog.appengine.Channel(token);
    var handler = {
        'onopen' : onOpened,
        'onmessage': onMessage,
        'onclose': onClosed,
        'onerror': onError
    };
    var socket = channel.open(handler);
    socket.onopen = onOpened;
    socket.onmessage = onMessage;
    socket.onclose = onClosed;
    socket.onerror = onError;
}


var roomState = 0;
setRoomVis = function(state){//---------------------------------------------------------Sets whether client is in a room
    if (state == "1"){//Entering a room
        $(".live_pugs").hide();
        $("#fade_room").hide();
        $(".create_room").hide();
        $(".pug_room").fadeIn();
    }else{
        $(".live_pugs").fadeIn();
        $("#fade_room").fadeIn();
        $(".create_room").hide();
        $(".pug_room").hide();
    }
}
var room;
linkRooms = function(){//-------------------------------------------------------get id's of table rows and make them links to room.
    $('#pug_rooms_table tr').each(function(i){
        this.style.cursor = "hand";
        this.style.cursor = "pointer";
        $(this).click(function(){
            room = 'room='+ this.id;
            sendMessage('/enter', room);
            //-------------------------------------Main Page Elements
            setRoomVis("1");
            //-------------------------------------Room Elements
            $('#leave_room').click(function(){
                sendMessage('/leave', room);
                setRoomVis("0");
                $("#scout>#player").remove();
                $("#soldier>#player").remove();
                $("#pyro>#player").remove();
                $("#demo>#player").remove();
                $("#heavy>#player").remove();
                $("#medic>#player").remove();
                $("#engie>#player").remove();
                $("#sniper>#player").remove();
                $("#spy>#player").remove();
                $("#captain>#player").remove();
                $("#heavy>#player").append('<td id="player"></td><td id="player"></td><td id="player">LOADING...</td>');
            });
            //---------------------------disband
            $('#disband').click(function(){
                sendMessage('/disband', room);
            })
            //---------------------------class buttons
            $("#scout_img").click(function(){
                var message = "class=0&"+room;
                sendMessage('/toggle_class', message);
            });
            $("#soldier_img").click(function(){
                var message = "class=1&"+room;
                sendMessage('/toggle_class', message);
            });
            $("#pyro_img").click(function(){
                var message = "class=2&"+room;
                sendMessage('/toggle_class', message);
            });
            $("#demo_img").click(function(){
                var message = "class=3&"+room;
                sendMessage('/toggle_class', message);
            });
            $("#heavy_img").click(function(){
                var message = "class=4&"+room;
                sendMessage('/toggle_class', message);
            });
            $("#medic_img").click(function(){
                var message = "class=5&"+room;
                sendMessage('/toggle_class', message);
            });
            $("#engie_img").click(function(){
                var message = "class=6&"+room;
                sendMessage('/toggle_class', message);
            });
            $("#sniper_img").click(function(){
                var message = "class=7&"+room;
                sendMessage('/toggle_class', message);
            });
            $("#spy_img").click(function(){
                var message = "class=8&"+room;
                sendMessage('/toggle_class', message);
            });
            //$("#captain_img").click(function(){
            //    var message = "class=9&"+room;
            //    sendMessage('/toggle_class', message);
            //});
            $("#scout_img_red").click(function(){
                var message = "class=9&"+room;
                sendMessage('/toggle_class', message);
            });
            $("#soldier_img_red").click(function(){
                var message = "class=10&"+room;
                sendMessage('/toggle_class', message);
            });
            $("#pyro_img_red").click(function(){
                var message = "class=11&"+room;
                sendMessage('/toggle_class', message);
            });
            $("#demo_img_red").click(function(){
                var message = "class=12&"+room;
                sendMessage('/toggle_class', message);
            });
            $("#heavy_img_red").click(function(){
                var message = "class=13&"+room;
                sendMessage('/toggle_class', message);
            });
            $("#medic_img_red").click(function(){
                var message = "class=14&"+room;
                sendMessage('/toggle_class', message);
            });
            $("#engie_img_red").click(function(){
                var message = "class=15&"+room;
                sendMessage('/toggle_class', message);
            });
            $("#sniper_img_red").click(function(){
                var message = "class=16&"+room;
                sendMessage('/toggle_class', message);
            });
            $("#spy_img_red").click(function(){
                var message = "class=17&"+room;
                sendMessage('/toggle_class', message);
            });
        });
    });
}




onOpened = function(){//--------------------------------------------------------
    //alert('Channel Open.');
    $("#chat_box").append('channel open<br>');
}
onClosed = function(){//--------------------------------------------------------
    //alert('Channel Closed.');
    $("#chat_box").append('Channel closed. Please refresh the page.<br>');
}
onError = function(){//---------------------------------------------------------
    //$("#chat_box").append('Channel error. Please refresh the page.<br>');
}
onMessage = function(m){//------------------------------------------------------
    newData = JSON.parse(m.data)
    //alert(m.data);
    if (newData.type == "room"){//----------------------------------------------room
        //alert("room incoming")
        if (newData.mic == "True")
            var mic_req = "<img alt='Microphone Required' src='/images/mic.png'> Required";
        else
            var mic_req = "";
        var table_row = "<tr id='" + newData.number + "'>" +
                        "<td>" + newData.name + "</td>" +
                        "<td>" + newData.level + "</td>" +
                        "<td>" + newData.style + "</td>" +
                        "<td>" + mic_req + "</td>" +
                        "</tr>";
        $("#pug_rooms_table").append(table_row);

        linkRooms();

    }else if (newData.type == "remove_room"){//---------------------------------remove_room
        var room = "#"+newData.room
        $(room).remove();
    }else if (newData.type == "update_room"){//---------------------------------update_room
    }else if (newData.type == "quit"){//----------------------------------------Makes user go to main page
        setRoomVis("0");
        alert(newData.reason);
    }else if (newData.type == "room_info"){//---------------------------------------update room with info
        $("#room_name h4").html(newData.name);
        $("#room_id").html(newData.id);
        $("#leader_name").html(newData.leader);
        $("#room_map").html(newData.level);
        if (newData.disband == false)
            $("#disband").hide();
    }else if (newData.type == "ready"){//---------------------------------------ready box popup
        $(".ready_box").fadeIn();
        $("#disband").hide();
        $("#leave_room").hide();
        $(".ready_box").click(function(){
            var room_id = $("#room_id").html();
            roomMessage = 'room=' + room_id;
            sendMessage('/ready', roomMessage);
            //alert(roomMessage);
            $(".ready_box").hide()
        });
    }else if (newData.type == "popup"){//---------------------------------------pop-up with text
        alert(newData.message);
    }else if (newData.type == "chat"){//----------------------------------------chat
        var $box = $("#chat_box").text();
        $("#chat_box").append("<b><span style='"+newData.color+"'>"+newData.sender+":</span></b> "+newData.message + "<br>");
        //scroll to bottom on message recieved if not scrolled
        if ($('#chat_box')[0].scrollHeight < $('#chat_box').scrollTop()+$('#chat_box').height()+20)
            $('#chat_box').scrollTop($('#chat_box')[0].scrollHeight);
        //update member count
        if ($("#chat_number").text() != ("("+newData.member_count+")"))
            $("#chat_number").html("("+newData.member_count+")").hide().fadeIn();

    }else{//--------------------------------------------------------------------Check for multi JSON
        if (newData[0].type == "update_room" || newData[0].type == "update_end"){
            $("#scout>#player").remove();
            $("#soldier>#player").remove();
            $("#pyro>#player").remove();
            $("#demo>#player").remove();
            $("#heavy>#player").remove();
            $("#medic>#player").remove();
            $("#engie>#player").remove();
            $("#sniper>#player").remove();
            $("#spy>#player").remove();
            $("#captain>#player").remove();

            $("#scout_red>#player").remove();
            $("#soldier_red>#player").remove();
            $("#pyro_red>#player").remove();
            $("#demo_red>#player").remove();
            $("#heavy_red>#player").remove();
            $("#medic_red>#player").remove();
            $("#engie_red>#player").remove();
            $("#sniper_red>#player").remove();
            $("#spy_red>#player").remove();
            $("#captain_red>#player").remove();
            var i=0;
            for (; newData[i].type != "update_end"; i++){
                //$("#chat_box").append(newData[0].type +"<br>");
                translate_classes(newData[i].classes);
                $(class_ids).append('<td id="player">'+ newData[i].alias +'</td>');
                //$("#chat_box").append("update end" +"<br>");
            }
            if (newData[i].type == "update_end"){
                translate_classes(newData[i].classes);
                $(class_ids).append('<td id="player">'+ newData[i].alias +'</td>');
            }

        }else{//----------------------------------------------------------------Invaid message
            $("#chat_box").append("Invalid Message Recieved!<br>");
        }
    }
}

$(document).ready(function(){
    openChannel();
    timeout();//channel timeout warning
    linkRooms();//make active rooms links
    //rotate tf_logo---------------------------
    var rot=0;
    self.setInterval ( function (e) {
        rot += 0.25;
        $('#tf_logo img').rotate(rot);
    }, 50 );
    //-----------------------------------------

    //footer display---------------------------
    $('.footer').delay(7000).fadeOut(function(){
        $('#tf2_pugs').mouseenter(function(){
            $('.footer').fadeIn();
        });
        $('#tf2_pugs').mouseleave(function(){
            $('.footer').fadeOut();
        });
    });


    $('#message').keypress(function(event){
        if (event.which == 13){
            var $message = $.trim($("#message").val());
            $("#message").val("");
            var $data = "message=" + $message + "&sender=" + nickname + "&room=main";
            var $box = $("#chat_box").text();
            if ($message !== ""){
                sendMessage('/chat', $data);
            }
        }
    });

    //TEMPORYARY####################
    //$("#fade_room").hide();
    //$(".live_pugs").hide();
    $(".pug_room").hide();
    $(".ready_box").hide();
    //################################

    $(".create_room").hide();
    $("#fade_room").click(function(){
        $(".create_room").fadeToggle();
    });

    $("#r_mumble").click(function(){
        $(".mumble_open").fadeToggle();
    });

    $("#chat_box").height(200);

    $("#create_room_button").click(function(){
        var r_name  = $('#r_name').val();
        var r_ip    = $('#r_ip').val();
        var r_rcon  = $('#r_rcon').val();
        var r_pass  = $('#r_pass').val();
        var r_map   = $('#r_map').val();
        var r_type  = $('#r_type option:selected').val();

        if ($('#r_spec').is(':checked')){
            var r_spec  = "True";
        }else{
            var r_spec  = "False";
        }
        if ($('#m_req').is(':checked')){
            var m_req  = "True";
        }else{
            var m_req  = "False";
        }

        var m_ip    = $('#m_ip').val();
        var m_port  = $('#m_port').val();
        var m_pass  = $('#m_pass').val();

        //mumble://[alias]:[pass]@[server]:[port]/?version=1.2.0
        //mumble://[alias]@[server]:[port]/?version=1.2.0
        alias = removeSpecialChar(alias);
        if (m_pass == ""){ //no password
            var m_alias = alias;
        }else{
            var m_alias = alias + ":";
        }

        var r_data  = "name=" + r_name +
                    "&ip=" + r_ip +
                    "&rcon=" + r_rcon +
                    "&pass=" + r_pass +
                    "&map=" + r_map +
                    "&type=" + r_type +
                    "&req=" + m_req +
                    "&mumble=" + m_alias + m_pass + "@" + m_ip + ":" + m_port +
                    "&spec=" + r_spec;

        sendMessage('/create', r_data);
        //$('#r_name').val("");$('#r_ip').val("");$('#r_rcon').val("");$('#r_pass').val("");$('#r_map').val("");
        //$('#m_ip').val("");$('#m_port').val("");$('#m_pass').val("");
        $(".create_room").fadeToggle();
    });

    $('#m_req').click(function(){
        $('#mumble_open').fadeToggle();
    });

    $(function() {
        var moveLeft = 20;
        var moveDown = 10;
        $('p#version').hover(function(e) {
            $('div#version_popup').show();
            }, function() {
                $('div#version_popup').hide();
        });
        $('#version').mousemove(function(e) {
            $("div#version_popup").css('top', e.pageY + moveDown).css('left', e.pageX + moveLeft);
        });
    });

    //--------------------------------------------------------------------------


});//--end ready--

window.onbeforeunload = function() {
    //leave room
    sendMessage('/leave', room);
}









