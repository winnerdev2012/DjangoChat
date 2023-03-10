
$(function() {
    document.querySelector('#chat-bar__input-content').focus();
    document.querySelector('#chat-bar__input-content').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-bar__send').click();
        }
    };

    document.querySelector('#chat-bar__send').onclick = function(e) {
        var input_mess = document.querySelector('#chat-bar__input-content');
        message = input_mess.value
        console.log(message)
        input_mess.value = ""
    };
});



