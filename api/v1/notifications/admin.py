from django.contrib import admin

from api.v1.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    fields = ('report', 'desc')

    def has_change_permission(self, request, obj=None):
        return False
