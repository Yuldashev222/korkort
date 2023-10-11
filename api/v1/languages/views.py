from django.utils.decorators import method_decorator
from rest_framework.generics import ListAPIView
from django.views.decorators.cache import cache_page

from api.v1.languages.models import Language
from api.v1.languages.serializers import LanguageSerializer


class LanguageAPIView(ListAPIView):
    permission_classes = ()
    queryset = Language.objects.filter(is_active=True)
    serializer_class = LanguageSerializer

    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
