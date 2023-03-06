from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.urls import reverse

from friends.models import FriendList, RequestFriend
from user.models import CustomUser
from chatroom.models import ChatRoom

# Create your views here.

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

class FriendBaseView(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL
    redirect_field_name = settings.LOGIN_URL
    
class FriendListView(FriendBaseView):
    def get(self, request, user_id):
        context = {}
        user = request.user
        if user_id:
            try:
                this_user = CustomUser.objects.get(pk=user_id)
                context['this_user'] = this_user
            except CustomUser.DoesNotExist:
                return HttpResponse("That user does not exist.")

class RequestFriendView(FriendBaseView):
    def post(self, request, receiver_user_id):
        context = {}
        sender_user = request.user
        try:
            receiver_user = CustomUser.objects.get(pk=receiver_user_id)
            context['user_profile'] = receiver_user
        except CustomUser.DoesNotExist:
            return HttpResponse("Receiver User does not exist.")
        if request.method == "POST":
            data = request.POST
            action = data.get("profile_action")
            
            # ADDFRIEND BUTTON
            if action == "add_friend":
                try:
                    # get all friend request
                    friend_requests = RequestFriend.objects.filter(sender=sender_user, receiver=receiver_user)
                    # find active request if have
                    try:
                        for friend in friend_requests:
                            if friend.is_active:
                                raise Exception("You already send them a friend request.")
                            
                        request_send = RequestFriend(sender=sender_user, receiver=receiver_user)
                        request_send.save()
                        context["result"] = "friend request sent"
                    except Exception as e:
                        context['result'] = e
                
                except RequestFriend.DoesNotExist:
                    request_send = RequestFriend(sender=sender_user, receiver=receiver_user)
                    request_send.save()
                    context["result"] = "friend request sent"
            
            # UNFRIEND BUTTON
            elif action == "unfriend":
                try:
                    removee = CustomUser.objects.get(pk=receiver_user)
                    friend_list = FriendList.objects.get(user=sender_user)
                    friend_list.unfriend(removee)
                    context['result'] = "Successfully removed that friend."
                except Exception as e:
                    context['result'] = f"Something went wrong: {str(e)}"
            
            # MESSAGE BUTTON
            elif action == "message":
                try:
                    friend_list = FriendList.objects.get(user=sender_user)
                except FriendList.DoesNotExist:
                    friend_list = FriendList(user=sender_user)
                    friend_list.save()
                
                if friend_list.is_mutual_friend(receiver_user):
                    room = ChatRoom.objects.filter(users__in=[sender_user, receiver_user], is_group_chat=False).first()
                    if room:
                        return redirect(reverse('chatroom:main_chat', kwargs={ 'room_id': room.pk }))
                    else:
                        room = ChatRoom(title=sender_user.username + "-" + receiver_user.username)
                        room.save()
                        room.connect_user(sender_user)
                        room.connect_user(sender_user)
                        room.save()
                        return redirect(reverse('chatroom:main_chat', kwargs={ 'room_id': room.pk }))
                else:
                    context['result'] = "you must be a friend to mess."
                
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
            # return redirect(reverse('user:user_profile', kwargs={ 'user_id': receiver_user_id })) 
            
class AcceptRequestFriend(FriendBaseView):
    def get(self, request):
        if is_ajax(request=request) and request.method == "GET":
            friend_request_id = request.GET.get("request_id", None)
            try:
                friend_request = RequestFriend.objects.get(pk=int(friend_request_id))
                friend_request.accept()
                friend_request.save()
            except RequestFriend.DoesNotExist:
                return HttpResponse({"error": "Request Friend Does Not Exist."}, status=200)
        else:
            return HttpResponse({"error": "Not GET request or not is ajax request"}, status=400)
        next = request.GET.get('next', '/')
        return HttpResponseRedirect(next)

class DeclineRequestFriend(FriendBaseView):
    def get(self, request, friend_request_id):
        try:
            friend_request = RequestFriend.objects.get(pk=friend_request_id)
            friend_request.decline()
            friend_request.save()
        except RequestFriend.DoesNotExist:
            return HttpResponse("Request Friend Does Not Exist.")