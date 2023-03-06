from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.

def get_profile_image_path(self):
    return f"profile_images/{self.pk}/{'profile_image.png'}"

def get_default_profile_image_path():
        # if self.gender:
        #     if self.gender == "Male":
        #         return "img/avt-male.svg"        
        return settings.STATIC_URL + "img/avt-female.svg"



GENDER_CHOICES = [
    ("Male", "Male"),
    ("Female", "Female")
]
class CustomUser(AbstractUser):
    # email = models.EmailField(_("Email Address"), unique=True)
    create_date = models.DateTimeField(verbose_name=_("created date"), auto_now_add=True)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_path
                                      , null=True, blank=True, default=get_default_profile_image_path)
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES, null=True, blank=True)

    # USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    
    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]