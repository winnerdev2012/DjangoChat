from rest_framework.serializers import ModelSerializer

from chatroom.models import ChatRoom

class ChatRoomSerializer(ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', ]