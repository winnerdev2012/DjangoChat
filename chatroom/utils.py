from django.utils.crypto import get_random_string
from django.db.models import Count

from chatroom.models import ChatRoom

def generate_id(length):
    return get_random_string(length)

def get_or_create_chat_room(users, is_group_chat=False):
    length = 7
    print("hahahahah")
    room = ChatRoom.objects.filter(users__in=users).annotate(num_users=Count('users')).filter(num_users=len(users))
    print("hahahahah")
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
    