from django.utils.decorators import method_decorator
from django.utils.translation import get_language
from django.views.decorators.cache import cache_page
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.accounts.permissions import IsStudent
from api.v1.levels.models import Level, LevelDetail
from api.v1.levels.serializers import LevelSerializer


class LevelAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['level_name_list'] = LevelDetail.objects.filter(language=get_language()).values('level', 'name', 'desc'
                                                                                            ).order_by('level_id')
        return ctx
