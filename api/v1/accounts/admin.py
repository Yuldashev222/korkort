from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'first_name', 'last_name', 'tariff_expire_date', 'date_joined', 'bonus_money', 'level', 'ball'
    ]
    list_display_links = ['email', 'first_name', 'last_name']
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['tariff_expire_date', 'date_joined']
    fields = [
        ('first_name', 'last_name'),
        'email',
        'user_code',
        'tariff_expire_date',
        'date_joined',
        'is_active',
        'is_verified',
        'bonus_money',
        'level',
        'level_image_id',
        'ball',
        'correct_answers',
        'completed_lessons',
        'last_exams_result',
        'avatar_id'
    ]
    readonly_fields = [
        'email',
        'date_joined',
        'avatar_id',
        'user_code',
        'bonus_money',
        'level',
        'level_image_id',
        'ball',
        'completed_lessons',
        'correct_answers',
        'last_exams_result',
        'tariff_expire_date',
    ]
    search_help_text = 'email, first_name, last_name'

    # inlines = []
    # raw_id_fields = ['']

    def get_queryset(self, request):
        return CustomUser.objects.filter(is_staff=False)
