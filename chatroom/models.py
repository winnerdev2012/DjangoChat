from django.db import models
from django.conf import settings
from django.db.models import Max, Count


# Create your models here.

class ChatRoomManager(models.Manager):
    def by_latest_message(self, user):
        rooms = ChatRoom.objects.filter(users__id=user).filter(is_active=True)
        rooms = rooms.annotate(latest_message_time=Max('message__timestamp')).order_by('-latest_message_time')
        return rooms
class ChatRoom(models.Model):

    title                   = models.CharField(max_length=255, blank=False, unique=True)
    users                   = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True ,help_text="user connected to the chat")
    timestamp               = models.DateTimeField(auto_now_add=True)  
    is_group_chat           = models.BooleanField(default=False) 
    is_active               = models.BooleanField(default=True)

    objects = ChatRoomManager()
    
    def __str__(self):
        return self.title
    
    def connect_user(self, user):
        """
        Return True if add user success
        """
        is_connected_user = False
        if not user in self.users.all():
            self.users.add(user)
            self.save()
            is_connected_user = True
        elif user in self.users.all():
            is_connected_user = True
        return is_connected_user
    
    def disconnect_user(self, user):
        """
        Return True if remove user success
        """
        is_removed_user = False
        if user in self.users.all():
            self.users.remove(user)
            self.save()
            is_removed_user = True
        elif user not in self.users.all():
            is_removed_user = True
        return is_removed_user
    
    def add_id_to_title(self):
        self.title = self.title + "-" + str(self.pk)
        self.save()
        
    def get_private_room_image(self, auth_user):
        if not self.is_group_chat:
            for user in self.users.all():
                if user != auth_user:
                    return user.profile_image.url  
            
            
    @property
    def room_name(self):
        """
        Return the channel room name that sockets should subscribe to and get mess from user
        """
        return f"ChatRoom-{self.title}"
        

class MessageManager(models.Manager):
    def by_room(self, room):
        messages = Message.objects.filter(room=room).order_by('-timestamp')    
        return messages
    
class Message(models.Model):
    user                        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message_body                = models.TextField(default='')
    parent_message_id           = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    room                        = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    is_read                     = models.BooleanField(default=False)
    timestamp                   = models.DateTimeField(auto_now_add=True)
    
    objects = MessageManager()
    
    def __str__(self):
        return self.message_body
        
    
