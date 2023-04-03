from django.urls import path

from chatroom.views import ChatRoomView, ChatRoomBlankView, IndexPageView


app_name = "chatroom"
urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('chatroom/home/', ChatRoomBlankView.as_view(), name='home'),
    path('chatroom/<int:room_id>/chat/', ChatRoomView.as_view(), name='main_chat'),
    # path('<int:friend_id>/', FindRoomView.as_view(), name="find_room")
]