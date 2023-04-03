import json

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from django.core.paginator import Paginator

from django.db.models import Count
from django.utils import timezone

from chatroom.exceptions import ClientError
from chatroom.models import ChatRoom, Message
from chatroom.utils import calculate_timestamp, LazyRoomChatMessageEncoder, LazyUserEncoder, LazyRoomEncoder
from chatroom.constants import *

from friends.models import FriendList
from user.models import CustomUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        # self.room_group_name = "chat_%s" % str(self.room_id)
        
        # print("ChatConsumer: connect: " + str(self.scope["user"]))
        await self.accept()
        
        # we can use "self.scope["url_route"]["kwargs"]["room_id"]" instead
        self.room_id = None
        # self.user_auth = self.scope["user"]
        # Join User friend group
        
    
    async def disconnect(self, close_code):
        # Leave room group
        print("ChatConsumer: disconnect")
        if self.scope["user"].is_authenticated:
            user = await update_user_status(self.scope["user"].id, False)
            await self.send_status(user.is_online)
        
        await self.channel_layer.group_discard(
            "user_connected",
            self.channel_name,
        )
        try:
            if self.room_id != None:
                await self.leave_room(self.room_id)
        except Exception as e:
            print("DISCONNECT EXCEPTION: " + str(e))

    async def receive(self, text_data):
        data_json = json.loads(text_data)
        command = data_json["command"]
        
        if command == "join":
            await self.join_room(data_json['room_id'])
        elif command == "leave":
            await self.leave_room(data_json['room_id'])
        elif command == "send":
            if len(data_json["message"].lstrip()) == 0:
                raise ClientError(422,"You can't send an empty message.")
            await self.send_message(data_json["message"], data_json["room_id"])
        elif command == "get_room_messages":
            room = await get_room_or_error(data_json['room_id'], self.scope["user"])
            data_dump = await get_room_messages(room)
            if data_dump != None:
                data_dump = json.loads(data_dump)
                await self.send_messages_to_ui(data_dump['messages'])
            else:
                raise ClientError(204,"Something went wrong retrieving the chatroom messages.")
        elif command == "get_user_auth":
            # await self.send(text_data=json.dumps({
            #     'user_auth': "user_auth",
            #     "user_id": self.scope["user"].id,
            #     "username": self.scope["user"].username
            # }))
            pass
        elif command == "get_room_list":
            data_dump = await get_room_list(self.scope["user"].id)
            if data_dump != None:
                data_dump = json.loads(data_dump)
                await self.send_room_list_to_ui(data_dump["private_rooms"], data_dump["group_rooms"])
            else:
                raise ClientError(204, "Something went wrong retrieving the room list.")
        
    async def send_message(self, message, room_id):
        
        if self.room_id != None:
            if str(room_id) != str(self.room_id):
                print("CLIENT ERRROR 1")
                raise ClientError("ROOM_ACCESS_DENIED", "Room access denied")
        else:
            print("CLIENT ERRROR 2")
            raise ClientError("ROOM_ACCESS_DENIED", "Room access denied")
        
        room = await get_room_or_error(room_id, self.scope["user"])
        
        await create_chat_message(room, self.scope['user'], message)
        
        await self.channel_layer.group_send(
            room.room_name, {
                'type': 'chat.message',
                'message': message,
                'username': self.scope['user'].username,
                'user_id': self.scope['user'].id,
                'profile_image': self.scope['user'].profile_image.url,
                'room_id': room_id,
            }
        )
        
        user_in_room = await get_users_in_room(room, self.scope["user"].id)
        
        if not user_in_room == None:
            await self.channel_layer.group_send(
                'user_connected', {
                'type': 'on.send',
                'user_receiver': user_in_room
            })
    
    async def join_room(self, room_id):
        
        try:
            room = await get_room_or_error(room_id, self.scope["user"])
        except ClientError as e:
            return await self.handle_client_error(e)
        
        # Add user to "users" list for room
        await connect_user(room, self.scope["user"])

        # Store that we're in the room
        self.room_id = room.id
        
        await self.channel_layer.group_add(
            "user_connected", self.channel_name
        )
        if self.scope["user"].is_authenticated:
            user = await update_user_status(self.scope["user"].id, True)
            await self.send_status(user.is_online)
        
        await on_user_connected(room, self.scope["user"])
        
        # Join room group
        await self.channel_layer.group_add(
            room.room_name, self.channel_name
        )
        
        await self.send(text_data=json.dumps({
            'join': str(self.room_id),
            'user_id': self.scope["user"].id
        }))
                
        if self.scope["user"].is_authenticated:
            # Notify the group that someone joined
            await self.channel_layer.group_send(
                room.room_name,
                {
                    "type": "type.join",
                    "room_id": room_id,
                    "profile_image": self.scope["user"].profile_image.url,
                    "username": self.scope["user"].username,
                    "user_id": self.scope["user"].id,
                }
            )
    
    async def leave_room(self, room_id):

        room = await get_room_or_error(room_id, self.scope["user"])

        # Remove user from "connected_users" list
        # await disconnect_user(room, self.scope["user"])

        # Notify the group that someone left
        await self.channel_layer.group_send(
            room.room_name,
            {
                "type": "type.leave",
                "room_id": room_id,
                "profile_image": self.scope["user"].profile_image.url,
                "username": self.scope["user"].username,
                "user_id": self.scope["user"].id,
            }
        )

        # Remove that we're in the room
        self.room_id = None

        # Remove them from the group so they no longer get room messages
        await self.channel_layer.group_discard(
            room.room_name,
            self.channel_name,
        )
        
        # Instruct their client to finish closing the room
        await self.send(text_data=json.dumps({
            "leave": str(room.id),
        }))

    async def send_messages_to_ui(self, messages):
        
        print("ChatConsumer: send_messages_to_ui. ")

        await self.send(text_data=json.dumps({
                "messages_payload": "messages_payload",
                "messages": messages,
        }))
        
    async def send_room_list_to_ui(self, private_rooms, group_rooms):
        print("ChatConsumer: send_room_list_to_ui. ")
        
        # print(private_rooms)
        # print(group_rooms)
        await self.send(text_data=json.dumps({
            "room_list": "room_list",
            "private_rooms": private_rooms,
            "group_rooms": group_rooms,
        }))
    
    async def send_status(self, status):
        
        print("SEND STATUS " + self.scope["user"].username + " is_online: " + str(status))
        
        await self.channel_layer.group_send(
            "user_connected",
            {
                "type": "type.status",
                "status": status,
                "user_id": self.scope["user"].id
            }
        )
    
    
    # TYPE for group send action
        
    async def chat_message(self, event):
        message = event["message"]

        timestamp = calculate_timestamp(timezone.now())
        print(timestamp)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'msg_type': MSG_TYPE_MESSAGE,
            'message': event['message'],
            'username': event['username'],
            'user_id': event['user_id'],
            'profile_image': event['profile_image'],
            'natural_timestamp': timestamp,
            'room_id': event['room_id'],
        }))
        
    async def type_join(self, event):
        """Called when user has joined chat: notify user

        Args:
            event (dict): from self.channel_layer.group_send action

        Returns:
            None:
        """
        if event["username"]:
            await self.send(text_data=json.dumps({
                'msg_type': MSG_TYPE_JOIN,
                'message': event['username'] + " connected!",
                'username': event['username'],
                'user_id': event['user_id'],
                'profile_image': event['profile_image'],
                'room_id': event['room_id']
            }))
            
    async def type_leave(self, event):
        """Called when user has left chat

        Args:
            event (dict): from self.channel_layer.group_send action

        Returns:
            None:
        """
        if event["username"]:
            await self.send(text_data=json.dumps({
                'msg_type': MSG_TYPE_LEAVE,
                'message': event['username'] + "disconnected!",
                'username': event['username'],
                'user_id': event['user_id'],
                'profile_image': event['profile_image'],
                'room_id': event['room_id']
            }))
            
    async def type_update(args):
        pass
    
    async def type_status(self, event):
        await self.send(text_data=json.dumps({
            "update_status": "update_status",
            "status": event["status"],
            "user_id": event["user_id"],
        }))
        
    async def on_send(self, event):
        await self.send(text_data=json.dumps({
            "on_send_action": "on_send_action",
            "user_receiver": event["user_receiver"]
        }))
            
    async def handle_client_error(self, e):
        """
        Called when a ClientError is raised.
        Sends error data to UI.
        """
        errorData = {}
        errorData['error'] = e.code
        if e.message:
            errorData['message'] = e.message
            await self.send(text_data=json.dumps(errorData))
        return
    
        

@database_sync_to_async
def create_chat_message(room, user, content):
    return Message.objects.create(user=user, room=room, message_body=content)

@database_sync_to_async
def get_room_or_error(room_id, user):
    try:
        room = ChatRoom.objects.get(pk=room_id)
    except ChatRoom.DoesNotExist:
        raise ClientError("ROOM_INVALID", "Invalid room.")

    # Is this user allowed in the room? (must be user1 or user2)
    if user not in room.users.all():
        raise ClientError("ROOM_ACCESS_DENIED", "You do not have permission to join this room.")

    # Are the users in this room friends?
    friend_list = FriendList.objects.get(user=user).friends.all()
    for usr in room.users.all():
        if usr != user and usr not in friend_list:
            raise ClientError("ROOM_ACCESS_DENIED", "You must be friends to chat.")
    return room

@database_sync_to_async
def get_users_in_room(room, user_id):
    for usr in room.users.all():
        if not usr.id == user_id:
            return usr.id
    return None  

@database_sync_to_async
def get_room_messages(room):
    try:
        data_send = {}
        msgs_qs = Message.objects.by_room(room=room)
        pages = Paginator(msgs_qs, DEFAULT_MSG_IN_ONE_PAGE)
        
        encoder = LazyRoomChatMessageEncoder()
        
        data_send['messages'] = encoder.serialize(msgs_qs) 
        
        return json.dumps(data_send)
        
    except Exception as e:
        print("GET_MESSAGES: " + str(e))
    return None

@database_sync_to_async
def get_room_list(user_id):
    try:
        data_send = {}
        rooms = ChatRoom.objects.by_latest_message(user_id)

        
        private_rooms = rooms.filter(is_group_chat=False)
        group_rooms = rooms.filter(is_group_chat=True)
        
        encoder = LazyRoomEncoder()
        
        data_send['private_rooms'] = encoder.serialize(private_rooms)
        data_send['group_rooms'] = encoder.serialize(group_rooms) 
        
        return json.dumps(data_send)
        
    except Exception as e:
        print("GET ROOM LIST:" + str(e))
    return None

# @database_sync_to_async
# def get_user_info(user_id):
#     try:
#         user_qs = CustomUser.objects.get(pk=user_id)
#         context = {}
#         encode = LazyUserEncoder()
#         context['user_info'] = encode.serialize(user_qs)
#         return json.dumps(context)
#     except Exception as e:
#         print("GET USER: " + str(e))

@database_sync_to_async
def disconnect_user(room, user):
    # remove from connected_users list
    account = CustomUser.objects.get(pk=user.id)
    return room.disconnect_user(account)

@database_sync_to_async
def connect_user(room, user):
    # add user to connected_users list
    account = CustomUser.objects.get(pk=user.id)
    return room.connect_user(account)

@database_sync_to_async
def on_user_connected(room, user):
    pass

@database_sync_to_async
def update_user_status(user_id, status):
    user = CustomUser.objects.get(id=user_id)
    user.update_user_status(status)
    return user