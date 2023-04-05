$(function() {
    var userMenuBtn = document.getElementById("header-profile-menu");
    var userMenu = document.getElementById("user-menu");

    userMenuBtn.addEventListener("click", function() {
        if (userMenu.style.display === 'none') {
            userMenu.style.display = 'flex';
        } else {
            userMenu.style.display = 'none';
        }
    })

    // document.addEventListener('click', function handleClickOutSiteUserMenu(event) {
    //     if (!userMenu.contains(event.target)) {
    //         userMenu.style.display = "none";
    //     }
    // })
});
hightLightPageSelected()

function hightLightPageSelected() {
    re_url = window.location.pathname;
    url_pieces = re_url.split("/");
    if (url_pieces[1] == "chatroom") {
        var item = document.getElementById("navbar-chat");
        item.classList.add("header__navbar-item--active");
    } else if (url_pieces[1] == "friends" || url_pieces[1] == "users") {
        var item = document.getElementById("navbar-contact");
        item.classList.add("header__navbar-item--active");
    }
}