from datetime import timedelta

from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication

from .models import CustomToken


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = CustomToken

        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed({'msg': 'Invalid token.'})

        if not token.user.is_verified:
            raise AuthenticationFailed({'msg': 'User has not confirmed email address.'})

        if not token.user.is_active or token.user.is_deleted:
            raise AuthenticationFailed({'msg': 'User inactive or deleted.'})

        if token.expires_at is not None and now() - token.created > timedelta(days=settings.TOKEN_EXPIRE_DAY):
            token.delete()
            raise AuthenticationFailed({'msg': 'Token has expired.'})

        return (token.user, token)


class SwaggerTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        if 'api/v1/docs' in request.path or 'api/v1/redoc' in request.path:
            token = request.GET.get('token')
            if token:
                return self.authenticate_credentials(token)
            else:
                raise AuthenticationFailed({'msg': 'Token is required to access Swagger documentation.'})

        return super().authenticate(request)
