from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUser(AbstractUser):
    # email = models.EmailField(_("Email Address"), unique=True)
    create_date = models.DateTimeField(auto_now_add=True)

    # USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
