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
    authentication_classes = []
    permission_classes = []
    serializer_class = LevelSerializer

    def get_queryset(self):
        return Level.objects.filter(leveldetail__language_id=get_language()).order_by('ordering_number')

    @method_decorator(cache_page(settings.CACHES['default']['TIMEOUT']))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['level_name_list'] = LevelDetail.objects.filter(language_id=get_language()
                                                            ).values('level_id', 'name'
                                                                     ).order_by('level__ordering_number')
        return ctx
