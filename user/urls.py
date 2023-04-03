from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from user.views import UserProfileView, SearchUserView

app_name = "user"

urlpatterns = [
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user_profile'),
    path('ajax/search/', SearchUserView.as_view(), name='ajax_search'),
]
