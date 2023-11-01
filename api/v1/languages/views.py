from django.conf import settings
from rest_framework.generics import ListAPIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from api.v1.languages.models import Language
from api.v1.languages.serializers import LanguageSerializer


class LanguageAPIView(ListAPIView):
    permission_classes = ()
    queryset = Language.objects.filter(is_active=True).order_by('ordering_number')
    serializer_class = LanguageSerializer

    @method_decorator(cache_page(settings.CACHES['default']['TIMEOUT']))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
