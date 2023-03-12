from django.urls import path, re_path

from chatroom.consumers import ChatConsumer

websocket_urlpatterns = [
    # path("ws/chatroom/<int:room_id>/chat/", ChatConsumer.as_asgi(), name="chat_room_ws"),
    re_path(r"ws/chatroom/(?P<room_id>\d+)/chat/$", ChatConsumer.as_asgi()),
]

