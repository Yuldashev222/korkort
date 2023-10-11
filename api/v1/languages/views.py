from rest_framework.generics import ListAPIView

from api.v1.languages.models import Language
from api.v1.languages.serializers import LanguageSerializer


class LanguageAPIView(ListAPIView):
    permission_classes = ()
    queryset = Language.objects.filter(is_active=True)
    serializer_class = LanguageSerializer
