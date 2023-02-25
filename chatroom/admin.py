from django.contrib import admin
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db import models

from chatroom.models import ChatRoom, Message

# Register your models here.

class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['id', 'title']
    list_filter = ['id']
    
    class Meta:
        model = ChatRoom
        

# Source http://masnun.rocks/2017/03/20/django-admin-expensive-count-all-queries/
# Modified version of a GIST I found in a SO thread
class CachingPaginator(Paginator):
    def _get_count(self):

        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)

            except:
                self._count = len(self.object_list)
        return self._count

    count = property(_get_count)


class MessageAdmin(admin.ModelAdmin):
    list_filter = ['room', 'user', 'timestamp']
    list_display = ['room', 'user', 'message_body', 'timestamp']
    search_field = ['room__title', 'user__username', 'message_body']
    readonly_field = ['id', 'user', 'timestamp']
    
    show_full_result_count = False
    paginator = CachingPaginator
    
    class Meta:
        model = Message

admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Message, MessageAdmin)