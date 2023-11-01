from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'first_name', 'last_name', 'tariff_expire_date', 'date_joined', 'bonus_money'
    ]
    list_display_links = ['email']
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['tariff_expire_date', 'date_joined']
    fields = [
        ('first_name', 'last_name'),
        'is_active',
        'is_verified',
        'email',
        'user_code',
        'tariff_expire_date',
        'date_joined',
        'bonus_money',
        'correct_answers',
        'completed_lessons',
        'avatar_id',
        'auth_provider'
    ]
    readonly_fields = [
        'email', 'date_joined', 'avatar_id', 'user_code', 'bonus_money',
        'completed_lessons', 'correct_answers', 'tariff_expire_date', 'is_verified', 'auth_provider'
    ]
    search_help_text = 'email, first_name, last_name'

    def get_queryset(self, request):
        return CustomUser.objects.filter(is_staff=False)
