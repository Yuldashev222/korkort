from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.accounts.models import CustomUser

from .models import CustomToken

from .serializers import (
    AuthTokenSerializer,
    RegisterSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    GoogleSignInSerializer, FacebookSignInSerializer, AppleSignInSerializer, PasswordResetCodeSerializer,
    CodePasswordResetConfirmSerializer
)
from api.v1.accounts.serializers import ProfileSerializer


# login view
class AuthTokenAPIView(GenericAPIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        CustomToken.objects.filter(user=user).delete()
        token = CustomToken.objects.create(user=user)
        user_data = ProfileSerializer(user).data
        return Response({'token': token.key, 'user': user_data}, status=status.HTTP_200_OK)


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
        if not user.is_deleted:
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


# facebook auth view
class FacebookSignInAPIView(CreateAPIView):
    permission_classes = ()
    serializer_class = FacebookSignInSerializer

    def perform_create(self, serializer):
        pass


class AppleSignInCallbackView(CreateAPIView):
    permission_classes = ()
    serializer_class = AppleSignInSerializer
