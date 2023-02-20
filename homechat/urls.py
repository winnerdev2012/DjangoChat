from django.urls import path

from .views import HomeChatView

app_name = "home_chat"

urlpatterns = [
    path('', HomeChatView.as_view(), name='home'),
]