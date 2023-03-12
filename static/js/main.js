
$(function() {

    const currentRoom = JSON.parse(document.getElementById("current-room").textContent);
    console.log(currentRoom);

    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chatroom/'
        + currentRoom
        + '/chat/'
    );

    document.querySelector('#chat-bar__input-content').focus();
    document.querySelector('#chat-bar__input-content').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-bar__send').click();
        }
    };

    document.querySelector('#chat-bar__send').onclick = function(e) {
        var input_mess = document.querySelector('#chat-bar__input-content');
        message = input_mess.value;
        console.log(message);
        input_mess.value = "";
    };

    var box_chat = document.getElementById("box_message");
    box_chat.scrollTop = box_chat.scrollHeight;
});



