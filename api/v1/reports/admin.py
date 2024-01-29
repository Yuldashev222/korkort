from django.contrib import admin

from api.v1.notifications.models import Notification
from api.v1.reports.models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('pk', 'student', 'lesson', 'question', 'report_type', 'created_at', 'is_completed', 'desc')
    list_filter = ('report_type', 'created_at', 'is_completed')
    select_related = ('student', 'lesson', 'question')  # last
    readonly_fields = ['student', 'lesson', 'question', 'report_type', 'desc', 'created_at']
    fields = [
        'student',
        'lesson',
        'question',
        'report_type',
        'desc',
        'created_at',
        'answer',
        'is_completed',
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj.is_completed:
            return self.fields
        return self.readonly_fields

    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):
        if obj.pk and obj.is_completed and not Report.objects.get(pk=obj.pk).is_completed:
            Notification.objects.create(notification_type=Notification.NOTIFICATION_TYPE[3][0],
                                        report_id=obj.pk,
                                        desc=obj.answer)
        super().save_model(request, obj, form, change)
