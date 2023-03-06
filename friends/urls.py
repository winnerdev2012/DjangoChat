from django.urls import path

from friends.views import RequestFriendView, AcceptRequestFriend, DeclineRequestFriend

app_name = "friends"

urlpatterns = [
    path('add/<int:receiver_user_id>/', RequestFriendView.as_view(),  name='friend_action'),
    path('accept/', AcceptRequestFriend.as_view(), name='accept_friend'),
    path('decline/', DeclineRequestFriend.as_view(), name='decline_friend'),
]