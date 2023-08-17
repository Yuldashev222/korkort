from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from api.v1.authentications.authentication import CustomTokenAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
    ),
    public=True,
    authentication_classes=(CustomTokenAuthentication,),
    permission_classes=(AllowAny,)
)
