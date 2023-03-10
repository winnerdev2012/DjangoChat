from django.contrib import admin

from friends.models import FriendList, RequestFriend
# Register your models here.

class FriendListAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_friends']
    list_filter = ['user']
    search_fields = ['user']
    # readonly_fields = ['user']
    def get_friends(self, obj):
        return "\n".join([f.username for f in obj.friends.all()])
    
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