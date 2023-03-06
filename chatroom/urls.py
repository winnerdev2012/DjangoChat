from django.urls import path

from chatroom.views import ChatRoomView, ChatRoomBlankView


app_name = "chatroom"
urlpatterns = [
    path('home/', ChatRoomBlankView.as_view(), name='home'),
    path('<int:room_id>/chat', ChatRoomView.as_view(), name='main_chat')
]