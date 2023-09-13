import requests
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator

from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.accounts.models import CustomUser
from api.v1.authentications.serializers.backend import AuthTokenSerializer, RegisterSerializer
from api.v1.authentications.serializers.google import GoogleSignInSerializer
from api.v1.authentications.serializers.password import (PasswordResetSerializer, PasswordResetCodeSerializer,
                                                         PasswordResetConfirmSerializer,
                                                         CodePasswordResetConfirmSerializer)


# login view
class AuthTokenAPIView(GenericAPIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# register view
class RegisterAPIView(CreateAPIView):
    permission_classes = (~IsAuthenticated,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('A confirmation link has been sent to your email')


# password reset view
class LinkPasswordResetView(CreateAPIView):
    permission_classes = ()
    serializer_class = PasswordResetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('The password reset link has been sent to the email', status=status.HTTP_200_OK)


# password reset view
class CodePasswordResetView(CreateAPIView):
    permission_classes = ()
    serializer_class = PasswordResetCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('The password reset code has been sent to the email', status=status.HTTP_200_OK)


# password reset confirm view
class LinkPasswordResetConfirmView(CreateAPIView):
    permission_classes = ()
    serializer_class = PasswordResetConfirmSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Your password has been successfully reset', status=status.HTTP_200_OK)


# password reset confirm view
class CodePasswordResetConfirmView(LinkPasswordResetConfirmView):
    serializer_class = CodePasswordResetConfirmSerializer


# verify email view
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.is_active = True
        user.save()
        return HttpResponse('<h1>Verification Success</h1>')

    return HttpResponse('<h1>Verification Failure</h1>')


# google auth view
class GoogleSignInAPIView(CreateAPIView):
    permission_classes = ()
    serializer_class = GoogleSignInSerializer

    def perform_create(self, serializer):
        pass


def facebook_login(request):
    redirect_uri = "%s://%s%s" % (request.scheme, request.get_host(), reverse('app:facebook_login'))
    code = request.GET.get('code')
    url = 'https://graph.facebook.com/v2.10/oauth/access_token'
    params = {
        'client_id': settings.FACEBOOK_CLIENT_ID,
        'client_secret': settings.FACEBOOK_CLIENT_SECRET,
        'code': code,
        'redirect_uri': redirect_uri,
    }
    response = requests.get(url, params=params)
    params = response.json()
    params.update({'fields': 'id,last_name,first_name,email'})
    url = 'https://graph.facebook.com/me'
    user_data = requests.get(url, params=params).json()
    email = user_data.get('email')

    if email:
        user, created = CustomUser.objects.get_or_create(email=email)

        if created:
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.auth_provider = 'facebook'
            user.is_verified = True
            user.set_password(None)

        elif not user.is_active:
            raise AuthenticationFailed('User inactive')

        elif not user.is_verified:
            user.is_verified = True

        user.save()
        # login(request, user)
    else:
        raise AuthenticationFailed('Unable to login with Facebook Please try again')
