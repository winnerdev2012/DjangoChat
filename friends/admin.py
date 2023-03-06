from django.contrib import admin

from friends.models import FriendList, RequestFriend
# Register your models here.

class FriendListAdmin(admin.ModelAdmin):
    list_display = ['user',]
    list_filter = ['user']
    search_fields = ['user']
    # readonly_fields = ['user']
    
    class Meta:
        model = FriendList
        

class RequestFriendAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver']
    list_filter = ['sender', 'receiver']
    search_fields = ['sender__username', 'sender__email', 'receiver__username', 'receiver__email']
    
    class Meta:
        model = RequestFriend
        


admin.site.register(FriendList, FriendListAdmin)
admin.site.register(RequestFriend, RequestFriendAdmin)