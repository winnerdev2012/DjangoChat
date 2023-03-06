from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from user.views import UserProfileView

app_name = "user"

urlpatterns = [
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user_profile')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)