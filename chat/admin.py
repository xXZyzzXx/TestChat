from django.contrib import admin

from chat.models import Message, Thread


class ThreadAdmin(admin.ModelAdmin):
    list_display = ("id", "get_participants", "created_at", "updated_at")

    def get_participants(self, obj):
        return obj.participants_names

    get_participants.short_description = "Participants"


class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "thread", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("text", "sender__username")


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message, MessageAdmin)
