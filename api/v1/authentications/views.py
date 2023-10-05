from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.accounts.models import CustomUser
from api.v1.authentications.serializers.apple import AppleSignInSerializer
from api.v1.authentications.serializers.backend import AuthTokenSerializer, RegisterSerializer, \
    ResendEmailVerifyLinkSerializer
from api.v1.authentications.serializers.facebook import FacebookSignInSerializer
from api.v1.authentications.serializers.google import GoogleSignInSerializer
from api.v1.authentications.serializers.password import (PasswordResetSerializer, PasswordResetCodeSerializer,
                                                         PasswordResetConfirmSerializer,
                                                         CodePasswordResetConfirmSerializer)


class AuthTokenAPIView(GenericAPIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterAPIView(CreateAPIView):
    permission_classes = (~IsAuthenticated,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response('A confirmation link has been sent to your email')


class ResendEmailVerifyLinkAPIView(RegisterAPIView):
    serializer_class = ResendEmailVerifyLinkSerializer

    def perform_create(self, serializer):
        pass


class LinkPasswordResetView(CreateAPIView):
    permission_classes = ()
    serializer_class = PasswordResetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('The password reset link has been sent to the email', status=status.HTTP_200_OK)


class CodePasswordResetView(CreateAPIView):
    permission_classes = ()
    serializer_class = PasswordResetCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('The password reset code has been sent to the email', status=status.HTTP_200_OK)


class LinkPasswordResetConfirmView(CreateAPIView):
    permission_classes = ()
    serializer_class = PasswordResetConfirmSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response('Your password has been successfully reset', status=status.HTTP_200_OK)


class CodePasswordResetConfirmView(LinkPasswordResetConfirmView):
    serializer_class = CodePasswordResetConfirmSerializer


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid, is_staff=False, is_verified=False, is_active=True)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.is_active = True
        user.save()
        return HttpResponse('<h1>Verification Success</h1>')

    return HttpResponse('<h1>Verification Failure</h1>')


class GoogleSignInAPIView(CreateAPIView):
    permission_classes = ()
    serializer_class = GoogleSignInSerializer

    def perform_create(self, serializer):
        pass


class FacebookSignInAPIView(GoogleSignInAPIView):
    serializer_class = FacebookSignInSerializer


class AppleSignInAPIView(GoogleSignInAPIView):
    serializer_class = AppleSignInSerializer
