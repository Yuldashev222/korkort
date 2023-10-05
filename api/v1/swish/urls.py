from django.core.cache import cache, caches
from django.urls import path
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.v1.accounts.models import CustomUser
from api.v1.swish.views import SwishCardAPIView

urlpatterns = [
    path('', SwishCardAPIView.as_view())
]
