from django.contrib import admin

from api.v1.swish.models import SwishCard


@admin.register(SwishCard)
class SwishCardAdmin(admin.ModelAdmin):
    list_display = ['number', 'student', 'created_at']
