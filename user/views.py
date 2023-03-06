from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from user.models import CustomUser
from friends.models import FriendList, RequestFriend

# Create your views here.

class UserBaseView(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL
    redirect_field_name = settings.LOGIN_URL

class UserProfileView(UserBaseView):
    """
    RELATIONSHIP:
        - [1]: is a friend
        - [2]: is not a friend
        - [0]: is yourself
    """
    
    def get(self, request, user_id):
        context = {}
        RELATIONSHIP = 1
        try:
            user_auth_friend_list, created = FriendList.objects.get_or_create(user=request.user)
            user_auth_request_list = RequestFriend.objects.filter(receiver=request.user, is_active=True)
            # user_auth_request_list = RequestFriend.objects.all()
            
            user_profile = CustomUser.objects.get(pk=user_id) # this user in profile page
            if request.user.id == user_id:
                RELATIONSHIP = 0
            elif user_auth_friend_list.is_mutual_friend(user_profile):
                RELATIONSHIP = 1
            else:
                RELATIONSHIP = 2
            context = {
                'user_profile': user_profile,
                'RELATIONSHIP': RELATIONSHIP,
                'user_auth_friend_list': user_auth_friend_list.friends.all(),
                'user_auth_request_list': user_auth_request_list,
            }
            
            return render(request, 'accounts/profile.html', context)
        except CustomUser.DoesNotExist:
            return HttpResponse("User does not exist")
        
        