
$(function() {

});
var chatSocket = null;
var userAuthId = null;
// get box chat

var box_chat = document.getElementById("box-message");
box_chat.scrollTop = box_chat.scrollHeight;

const currentRoom = JSON.parse(document.getElementById("current-room").textContent);

setupChatSocket(currentRoom)
hightLightRoomSelected(currentRoom)

function setupChatSocket(room_id) {

    // Correctly decide between ws:// and wss://
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";

    if (debug_mode == "True") {
        // development
        var ws_path = ws_scheme 
                    + '://' 
                    + window.location.host 
                    + '/ws/chatroom/' 
                    + room_id 
                    + '/chat/'; 
    } else {
        var ws_path = ws_scheme 
                    + '://' 
                    + window.location.host 
                    + ':8001/ws/chatroom/' 
                    + room_id 
                    + '/chat/'; 
    }
    chatSocket = new WebSocket(ws_path);

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);

        if (data.join) {
            console.log("Joining room " + data.join);
            // getUserAuth();
            getRoomChatMessages();
            userAuthId = data.user_id;
            // enableChatLogScrollListener()
        };

        if (data.leave) {
            // do nothing
            console.log("Leaving room " + data.leave);
        };
        
        if(data.messages_payload){
            handleMessagesInBox(data.messages, false)
        };

        if (data.msg_type == 0 || data.msg_type == 1 || data.msg_type == 2) {
            handleMessaging(data, true);
        }
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    chatSocket.onOpen = function(e){
        console.log("ChatSocket onOpen", e)
    }

    chatSocket.onerror = function(e){
        console.log('ChatSocket error', e)
    }

    chatSocket.addEventListener("open", function(e){
        console.log("ChatSocket OPEN")
        // join chat room
        if(is_user_auth == "True"){
            chatSocket.send(JSON.stringify({
                "command": "join",
                "room_id": room_id
            }));
        }
    });
}   

document.querySelector('#chat-bar__input-content').focus();
document.querySelector('#chat-bar__input-content').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-bar__send').click();
    }
};

document.querySelector('#chat-bar__send').onclick = function(e) {
    var input_mess = document.querySelector('#chat-bar__input-content');
    message = input_mess.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'command': "send",
        'room_id': currentRoom
    }));
    // console.log(message);
    input_mess.value = "";
};

function getRoomChatMessages() {
    console.log("get_room_messages ");
    chatSocket.send(JSON.stringify({
        "command": "get_room_messages",
        "room_id": currentRoom,
    }));
}

function hightLightRoomSelected(roomId) {
    var room_doc = document.getElementById("room__roomId-" + roomId);
    room_doc.classList.add("chatmenu-item--active");
}

function createMessSend(text, isNewMessage) {
    var msg = document.createElement("div");
    msg.classList.add("message-sent");

    msg_box = document.createElement("div");
    msg_box.classList.add("message-box");
    msg_box.classList.add("message-sent__body");

    msg_content = document.createElement("p");
    msg_content.classList.add("message-content");
    msg_content.innerHTML = text;

    msg_box.appendChild(msg_content);
    msg.appendChild(msg_box);

    if (!isNewMessage) {
        box_chat.insertBefore(msg, box_chat.firstChild);
    } else {
        box_chat.appendChild(msg);
    }

    box_chat.scrollTop = box_chat.scrollHeight;
};

function createMessReceived(text, isNewMessage) {
    var msg = document.createElement("div");
    msg.classList.add("message-received");

    msg_box = document.createElement("div");
    msg_box.classList.add("message-box");
    msg_box.classList.add("message-received__body");

    msg_content = document.createElement("p");
    msg_content.classList.add("message-content");
    msg_content.innerHTML = text;

    msg_box.appendChild(msg_content);
    msg.appendChild(msg_box);
    
    if (!isNewMessage) {
        box_chat.insertBefore(msg, box_chat.firstChild);
    } else {
        box_chat.appendChild(msg);
    }
    

    box_chat.scrollTop = box_chat.scrollHeight;
};

function handleMessagesInBox(messages, isNewMessage) {
    if(messages != null && messages != "undefined" && messages != "None"){
        messages.forEach(function(message){
            if (message.user_id == userAuthId) {
                createMessSend(message.message, isNewMessage);
            } else {
                createMessReceived(message.message, isNewMessage);
            }
            
        })
    }
}

function handleMessaging(data, isNewMessage) {
    messageType = data['msg_type']
    msg_id = data['msg_id']
    message = data['message']
    uName = data['username']
    user_id = data['user_id']
    profile_image = data['profile_image']
    timestamp = data['natural_timestamp']
    console.log("append chat message: " + messageType)

    switch(messageType) {
        case 0:
            if (user_id == userAuthId) {
                createMessSend(message, isNewMessage);
            } else {
                createMessReceived(message, isNewMessage);
            }
            break;
        case 1:
            break;
        case 2:
            break;
    }
}

function getUserAuth() {
    chatSocket.send(JSON.stringify({
        "command": "get_user_auth",
    }));
}


// window.addEventListener('scroll', function() {
//     var scrollPosition = window.scrollY;
//     var elementHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    
//     if (scrollPosition === 0) {
//       loadMoreData();
//     }
//   });
  
//   function loadMoreData() 


