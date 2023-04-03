import json
from django.utils.crypto import get_random_string
from datetime import datetime
from django.contrib.humanize.templatetags.humanize import naturalday
from django.db.models import Count
from django.core.serializers.python import Serializer

from chatroom.models import ChatRoom, Message
from chatroom.constants import *

def generate_id(length):
    return get_random_string(length)

def get_or_create_chat_room(users, is_group_chat=False):
    length = 7
    room = ChatRoom.objects.filter(users__in=users).annotate(num_users=Count('users')).filter(num_users=len(users))
    # is empty
    if not room:
        room = ChatRoom(title=get_random_string(length), is_group_chat=is_group_chat)
        room.save()
        room.add_id_to_title()
        for user in users:
            room.connect_user(user=user)
        room.save()
        return room
    else:
        # return only the first object in the query 
        return room.first()    
    
def calculate_timestamp(timestamp):
    """
	1. Today or yesterday:
		- EX: 'today at 10:56 AM'
		- EX: 'yesterday at 5:19 PM'
	2. other:
		- EX: 05/06/2020
		- EX: 12/28/2020
    """
    ts = ""
	# Today or yesterday
    if (naturalday(timestamp) == "today") or (naturalday(timestamp) == "yesterday"):
        str_time = datetime.strftime(timestamp, "%I:%M %p")
        str_time = str_time.strip("0")
        ts = f"{naturalday(timestamp)} at {str_time}"
	# other days
    else:
        str_time = datetime.strftime(timestamp, "%m/%d/%Y")
        ts = f"{str_time}"  
    return str(ts)
    
class LazyRoomChatMessageEncoder(Serializer):
    def get_dump_object(self, obj):
        dump_object = {}
        dump_object.update({'msg_type': MSG_TYPE_MESSAGE})
        dump_object.update({'msg_id': str(obj.id)})
        dump_object.update({'user_id': str(obj.user.id)})
        dump_object.update({'username': str(obj.user.username)})
        dump_object.update({'message': str(obj.message_body)})
        dump_object.update({'profile_image': str(obj.user.profile_image.url)})
        dump_object.update({'natural_timestamp': calculate_timestamp(obj.timestamp)})
        dump_object.update({'room_id': str(obj.room.id)})
        return dump_object
    
class LazyUserEncoder(Serializer):
    def get_dump_object(self, obj):
        dump_object = {}
        dump_object.update({'id': str(obj.id)})
        dump_object.update({'username': str(obj.username)})
        dump_object.update({'profile_image': str(obj.profile_image.url)})
        dump_object.update({'status': str(obj.is_online)})
        return dump_object
    
class LazyRoomEncoder(Serializer):
    def get_dump_object(self, obj):
        msg = ""
        last_mess = Message.objects.by_room(room=obj)
        if last_mess:
            msg = last_mess.first().message_body
        
        room_img = ""
        if not obj.is_group_chat:
            e = LazyUserEncoder()
            users = e.serialize(obj.users.all())     
            # room_img = json.dumps(users)
            room_img = users
            
        dump_object = {}
        dump_object.update({'id': str(obj.id)})
        dump_object.update({'title': str(obj.title)})
        dump_object.update({'timestamp': calculate_timestamp(obj.timestamp)})
        dump_object.update({'is_group_chat': str(obj.is_group_chat)})
        dump_object.update({'is_active': str(obj.is_active)})
        dump_object.update({'latest_message': msg})
        dump_object.update({'users': room_img})
        return dump_object