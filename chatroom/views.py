from django.shortcuts import render
from django.views.generic import View
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from chatroom.models import ChatRoom
from friends.models import FriendList

# Create your views here.

class ChatRoomBaseView(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL
    redirect_field_name = settings.LOGIN_URL
    
class IndexPageView(ChatRoomBaseView):
    def get(self, request):
        blank_path = reverse('chatroom:home')
        return redirect(blank_path)

class ChatRoomBlankView(ChatRoomBaseView):
    def get(self, request):
        context = {}
        user = request.user
        
        is_selected_room = False
        context['is_selected_room'] = is_selected_room
        
        rooms = ChatRoom.objects.by_latest_message(user.id)
        
        room_latest_path = reverse('chatroom:main_chat', kwargs={'room_id': rooms.first().id})
        return redirect(room_latest_path)
        
        # return render(request, 'pages/main.html', context)

class ChatRoomView(ChatRoomBaseView):
    def get(self, request, room_id):
        context = {}
        user = request.user
        room_id = int(room_id)
        
        is_selected_room = True
        context['is_selected_room'] = is_selected_room
             
        # room list
        room_list = ChatRoom.objects.filter(users__pk=user.pk, is_active=True)
        context['room_list'] = room_list
        context['debug_mode'] = settings.DEBUG
        
        # room selected
        room = ChatRoom.objects.get(pk=room_id)
        if room.is_group_chat == False:
            for room_user in room.users.all():
                if room_user.pk != user.pk:
                    context['chat_user_selected'] = room_user
             
        
        context['room'] = room
        return render(request, 'pages/main.html', context=context)
        