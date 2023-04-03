$(function() {
});
hightLightPageSelected()

function hightLightPageSelected() {
    re_url = window.location.pathname;
    url_pieces = re_url.split("/");
    if (url_pieces[1] == "chatroom") {
        var item = document.getElementById("navbar-chat");
        item.classList.add("header__navbar-item--active");
    } else if (url_pieces[1] == "friends") {
        var item = document.getElementById("navbar-contact");
        item.classList.add("header__navbar-item--active");
    }
}