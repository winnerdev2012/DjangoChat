from django.db import models

from user.models import CustomerUser


# Create your models here.

class Message(models.Model):
    creator_user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    subject = models.CharField(default='', max_length=255)
    message_body = models.TextField(default='')
    create_date = models.DateTimeField(auto_created=True)
    parent_message_id = models.ForeignKey('self', on_delete=models.CASCADE)

class MessageRecipient(models.Model):
    recipient_id = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    # recipient_group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)