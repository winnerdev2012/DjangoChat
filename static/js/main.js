
$(function() {
    searchSetup()
    function searchSetup() {
        var searchInput = document.getElementById("search-user-input");
        var searchForm = document.getElementById("search-form");
        var searchBlock = document.getElementById("chatmenu-navbar__search-wrap")
        var csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        
    
        searchInput.addEventListener("focus", function() {
            var result = document.querySelector(".chatmenu-navbar__search-result");
            result.style.display = "block";
        });

        document.addEventListener('click', function handleClickOutSiteSearch(event) {
            if (!searchBlock.contains(event.target)) {
                var result = document.querySelector(".chatmenu-navbar__search-result");
                result.style.display = "none";
            }
        })
        
        sendSearchUserRequest = (searchData) => {
            $.ajax({
                type: 'POST',
                url: '/users/ajax/search/',
                data: {
                    'csrfmiddlewaretoken': csrf,
                    'search_data': searchData,
                },
                success: (response) => {
                    console.log(response)
                    $(".chatmenu-navbar__search-list").empty();
                    if (typeof response.users == 'string' ) {
                        $("<li><span>" + response.users + "</span></li>").appendTo(".chatmenu-navbar__search-list");
                    } else {
                        response.users.forEach(function(user) {
                            createSearchUserItem(user.username, user.user_id, user.profile_image);
                        })
                    }
                },
                error: (response) => {
                    console.log(response)
                }
            });
        }
    
        searchInput.addEventListener("keyup", function(e) {
            console.log(e.target.value);
            sendSearchUserRequest(e.target.value);
            // var result = document.querySelector(".chatmenu-navbar__search-result");
            // result.style.display = "block";
        });
    }

    function createSearchUserItem(username, userId, profileImage) {
        var searchList = document.getElementsByClassName("chatmenu-navbar__search-list");
        var searchInput = document.getElementById("search-user-input");
        var searchItem = document.createElement("li");
        searchItem.classList.add("chatmenu-navbar__search-item");

        var searchItemLink = document.createElement("a");
        searchItemLink.classList.add("chatmenu-navbar__search-link");
        searchItemLink.href = "/users/profile/" + userId + "/";

        searchItem.appendChild(searchItemLink);

        var searchItemImage = document.createElement("img");
        searchItemImage.classList.add("chatmenu-navbar__search-image");
        searchItemImage.src = profileImage;

        var searchItemUsername = document.createElement("span");
        searchItemUsername.classList.add("chatmenu-navbar__search-item-info");
        searchItemUsername.innerHTML = username;

        searchItemLink.appendChild(searchItemImage);
        searchItemLink.appendChild(searchItemUsername);

        searchList[0].appendChild(searchItem);

    }
    
});
var chatSocket = null;
var userAuthId = null;
// get box chat
var box_chat = document.getElementById("box-message");
box_chat.scrollTop = box_chat.scrollHeight;

const currentRoom = JSON.parse(document.getElementById("current-room").textContent);

setupChatSocket(currentRoom)

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
            getRoomList();
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

        if (data.room_list) {
            handleRoomList(data.private_rooms, data.group_rooms);
        }

        if (data.update_status) {
            console.log(data.status);
            updateStatus(data.user_id, data.status);
        }

        if (data.on_send_action) {
            if (data.user_receiver == userAuthId) {
                clearRoomList();
                getRoomList();
            }
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

function getRoomList() {
    chatSocket.send(JSON.stringify({
        "command": "get_room_list",
    }))
}

function handleMessagesInBox(messages, isNewMessage) {
    // [0]: sender; [1]: receiver 
    if(messages != null && messages != "undefined" && messages != "None"){
        messages.forEach(function(message){
            if (message.user_id == userAuthId) {
                createMess(message.message, message.profile_image, message.username, message.natural_timestamp, 0, isNewMessage);
            } else {
                createMess(message.message, message.profile_image, message.username, message.natural_timestamp, 1, isNewMessage);
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
    room_id = data['room_id']
    console.log("append chat message: " + messageType)

    switch(messageType) {
        case 0:
            if (user_id == userAuthId) {
                createMess(message, profile_image, uName, timestamp, 0, isNewMessage);
            } else {
                createMess(message, profile_image, uName, timestamp, 1, isNewMessage);
            }
            onNewMess(room_id, message);
            // getRoomList();
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

function handleRoomList(private_rooms, group_rooms) {
    if (private_rooms != null && private_rooms != "undefined" && private_rooms != "None") {
        private_rooms.forEach(function(room) {
            appendPrivateRoom(room)
        })
    }

    if (group_rooms != null && group_rooms != "undefined" && group_rooms != "None") {
        group_rooms.forEach(function(room) {
            appendGroupRoom(room);
        })
    }
    hightLightRoomSelected(currentRoom)
}

function clearRoomList() {
    var list_room = document.getElementById("private-chat__list");
    var delChild = list_room.lastChild
    while (delChild) {
        list_room.removeChild(delChild);
        delChild = list_room.lastChild;
     }
}

function onNewMess(room_id, message) {
    var list_room = document.getElementById("private-chat__list");
    
    var list_item = document.getElementById("room__li-" + room_id);


    var latest = document.getElementById("latest-message__roomId-" + room_id);
    latest.innerHTML = message;

    list_room.removeChild(list_item);
    list_room.insertBefore(list_item, list_room.firstChild);

}

function updateStatus(user_id, status) {
    var status_icon = document.getElementById("room-status-userId-" + user_id);
    var status_in_room_selected = document.getElementById("status-userId-" + user_id)
    if (status) {
        status_icon.style.color = "green";
        status_in_room_selected.style.color = "green"
        status_in_room_selected.innerHTML = "<i class='fa-solid fa-circle'></i> Online";
    } else {
        status_icon.style.color = "var(--text-color)";
        status_in_room_selected.style.color = "var(--text-color)";
        status_in_room_selected.innerHTML = "<i class='fa-solid fa-circle'></i> Offline";
    }
}


// window.addEventListener('scroll', function() {
//     var scrollPosition = window.scrollY;
//     var elementHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    
//     if (scrollPosition === 0) {
//       loadMoreData();
//     }
//   });
  
//   function loadMoreData() 

function appendPrivateRoom(room) {
    console.log(room.users)
    var list_room = document.getElementById("private-chat__list");

    var list_item = document.createElement("li");
    list_item.id = "room__li-" + room.id

    var list_link = document.createElement("a"); 
    list_link.classList.add("chatmenu-item");
    list_link.id = "room__roomId-" + room.id;
    list_link.href = "/chatroom/" + room.id + "/chat/";

    var status_icon = document.createElement("i");
    status_icon.classList.add("fa-solid")
    status_icon.classList.add("fa-circle");
    status_icon.classList.add("chatmenu-status");

    var room_img = document.createElement("img");
    room_img.classList.add("chatmenu-info__avatar");

    var username = document.createElement("h4");
    username.classList.add("chatmenu-info__username");

    room.users.forEach(function(user){
        if (user.id != userAuthId) {
            // room_img.src = user.profile_image;
            room_img.style.backgroundImage = "url('" + user.profile_image + "')";
            status_icon.id = "room-status-userId-" + user.id;
            username.innerHTML = user.username;
            if (user.status == "True") {
                status_icon.style.color = "green";
            } else {
                status_icon.style.color = "#ccc";
            }
        }
    })
    

    var menu_info = document.createElement("div");
    menu_info.classList.add("chatmenu-info");
    
    var latest = document.createElement("p");
    latest.classList.add("chatmenu-info__lastest");
    latest.id = "latest-message__roomId-" + room.id;
    latest.innerHTML = room.latest_message;



    menu_info.appendChild(username);
    menu_info.appendChild(latest);

    list_link.appendChild(room_img);
    list_link.appendChild(menu_info);
    list_link.appendChild(status_icon);

    list_item.appendChild(list_link);

    list_room.appendChild(list_item);
}

function appendGroupRoom(room) {
    var list_room = document.getElementsByClassName("group-chat__list");
}


function createMess(message, imgUrl, username, timestamp, messOwner, isNewMessage) {
    var msg = document.createElement("div");

    msg_img = document.createElement("img");
    msg_img.classList.add("message-avatar");
    // msg_img.src = imgUrl
    msg_img.style.backgroundImage = "url('" + imgUrl + "')";

    msg_container = document.createElement("div");
    msg_container.classList.add("message-container");

    msg_info = document.createElement("div");
    msg_info.classList.add("message-info");

    msg_info_usrname = document.createElement("span");
    msg_info_usrname.classList.add("message-info__username");
    msg_info_usrname.innerHTML = username;

    msg_info_time = document.createElement("span");
    msg_info_time.classList.add("message-info__timestamp");
    msg_info_time.innerHTML = timestamp;

    msg_info.appendChild(msg_info_usrname);
    msg_info.appendChild(msg_info_time);

    msg_box = document.createElement("div");
    msg_box.classList.add("message-box");

    msg_content = document.createElement("p");
    msg_content.classList.add("message-content");
    msg_content.innerHTML = message;

    // [0]: message sent. [1]: message receiver
    if (messOwner == 0) {
        msg.classList.add("message-sent");
        msg_box.classList.add("message-sent__body");
    } else {
        msg.classList.add("message-received");
        msg_box.classList.add("message-received__body");
    }

    msg_box.appendChild(msg_content);

    msg_container.appendChild(msg_info);
    msg_container.appendChild(msg_box);

    msg.appendChild(msg_img);
    msg.appendChild(msg_container);
    
    if (!isNewMessage) {
        box_chat.insertBefore(msg, box_chat.firstChild);
    } else {
        box_chat.appendChild(msg);
    }

    box_chat.scrollTop = box_chat.scrollHeight;
};
