# from django.contrib import admin
#
# from api.v1.balls.models import TestBall
#
#
# @admin.register(TestBall)
# class TestBallAdmin(admin.ModelAdmin):
#     list_display = ['ball']
#
#     def has_add_permission(self, request):
#         return not TestBall.objects.exists()
#
#     def has_delete_permission(self, request, obj=None):
#         return False
