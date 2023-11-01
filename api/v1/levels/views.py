from django.conf import settings
from rest_framework.generics import ListAPIView
from django.utils.decorators import method_decorator
from django.utils.translation import get_language
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.cache import cache_page

from api.v1.levels.models import Level, LevelDetail
from api.v1.levels.serializers import LevelSerializer
from api.v1.accounts.permissions import IsStudent


class LevelAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

    @method_decorator(cache_page(settings.CACHES['default']['TIMEOUT']))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['level_name_list'] = LevelDetail.objects.filter(language_id=get_language()).values('level', 'name', 'desc'
                                                                                            ).order_by('level_id')
        return ctx
