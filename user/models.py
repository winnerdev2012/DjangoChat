from django.db import models
from django.contrib.auth.models import AbstractUser, Group

# Create your models here.

class CustomerUser(AbstractUser):
    is_active = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_created=True)