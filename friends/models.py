from django.db import models
from django.conf import settings

# Create your models here.

class FriendList(models.Model):
    user                = models.OneToOneField(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, related_name='user')
    
    friends             = models.ManyToManyField(settings.AUTH_USER_MODEL,
        blank=True, related_name='friends')
    
    
    def __str__(self):
        return self.user.username
    
    def add_friend(self, account):
        """
        ADD a friend
        Args:
            account (user): account add to list friend
        """
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()
            
    def remove_friend(self, account):
        """
        REMOVE a friend
        Args:
            account (user): account remove
        """
        if account in self.friends.all():
            self.friends.remove(account)
            
    
    def unfriend(self, removee):
        """
        Unfriending someone
        Args:
            removee (user):
        """
        remover_friend_list = self.friends
        remover_friend_list.remove_friend(removee)
        
        friend_list = FriendList.objects.get(user=removee)
        friend_list.remove_friend(self.user)
        
        
    def is_mutual_friend(self, friend):
        """
        Is this a friend
        """
        if friend in self.friends.all():
            return True
        return False
    
    
    
class RequestFriend(models.Model):
    sender              = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='sender')
    
    receiver            = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='receiver')
    
    is_active           = models.BooleanField(blank=True, null=False, default=True)
    
    timestamp           = models.DateTimeField(auto_now_add=True)    
    
    def __str__(self):
        return self.sender.username
    
    def accept(self):
        """
        Accept a friend request
        update (sender, receiver) friend list
        """
        
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()
    
    
    def decline(self):
        """
        Decline a friend request
        ->setting "is_active" 
        """
        self.is_active = False
        self.save()
        
        
    def cancel(self):
        """
        Cancel a friend request 
        -> like decline function but send a notification
        """
        
        self.is_active = False
        self.save()
        
        