from django.shortcuts import render
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from friends.models import FriendList

# Create your views here.

class ChatRoomBaseView(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL
    redirect_field_name = settings.LOGIN_URL

class ChatRoomBlankView(ChatRoomBaseView):
    def get(self, request):
        context = {}
        friend_list, created = FriendList.objects.get_or_create(user=request.user)
        is_selected_room = False
        context['is_selected_room'] = is_selected_room
        context['friend_list'] = friend_list
        return render(request, 'pages/main.html', context)

class ChatRoomView(ChatRoomBaseView):
    def get(self, request, room_id):
        context = {}
        user = request.user
        friend_list, created = FriendList.objects.get_or_create(user=user)
        is_selected_room = True
        context['is_selected_room'] = is_selected_room
        context['friend_list'] = friend_list
        return render(request, 'pages/main.html', context=context)