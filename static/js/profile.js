
$(function() {
    // lấy phần Modal
    var modal = document.getElementById('modal');

    // Lấy phần button mở Modal
    var friend_list_btn = document.getElementById("friend_list_btn");
    var request_list_btn = document.getElementById("request_list_btn");

    var friend_list_content = document.getElementById("friend_list_list");
    var request_list_content = document.getElementById("friend_request_list");

    var accept_btn = document.getElementById("accept_btn");
    var decline_btn = document.getElementById("decline_btn");

    // Lấy phần span đóng Modal
    var close_list_btn = document.getElementById("close_list_btn");
    var extra_list_title = document.getElementById("extra-list__title");

    // Khi button được click thi mở Modal

    friend_list_btn.onclick = function() {
        modal.style.display = "flex";
        friend_list_content.style.display = "flex";
        request_list_content.style.display = "none";
        extra_list_title.innerHTML = "Friends List"
    }

    // Khi span được click thì đóng Modal
    close_list_btn.onclick = function() {
        modal.style.display = "none";
    }

    // Khi click ngoài Modal thì đóng Modal
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // // accept request friend
    // accept_btn.onclick = function() {
    //     const requestObj = XMLHttpRequest()
    //     requestObj.onreadystatechange = function () {
    //         if (this.readystate == 4 && this.status == 200) {
    //             console.log(this.responseText)
    //         }

    //         requestObj.open("GET", "{% url 'friends:accept_friend' %}")
    //     }
    // }
    
    

    // $("#id_nick_name").focusout(function (e) {
    //     e.preventDefault();
    //     // get the nickname
    //     var nick_name = $(this).val();
    //     // GET AJAX request
    //     $.ajax({
    //         type: 'GET',
    //         url: "{% url 'validate_nickname' %}",
    //         data: {"nick_name": nick_name},
    //         success: function (response) {
    //             // if not valid user, alert the user
    //             if(!response["valid"]){
    //                 alert("You cannot create a friend with same nick name");
    //                 var nickName = $("#id_nick_name");
    //                 nickName.val("")
    //                 nickName.focus()
    //             }
    //         },
    //         error: function (response) {
    //             console.log(response)
    //         }
    //     })
    // })
    request_list_btn.onclick = function() {
        modal.style.display = "flex";
        friend_list_content.style.display = "none";
        request_list_content.style.display = "flex";
        extra_list_title.innerHTML = "Request List"
    }
 });


