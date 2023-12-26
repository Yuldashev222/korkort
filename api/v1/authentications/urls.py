from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    # path('email-verify/resend/', views.ResendEmailVerifyLinkAPIView.as_view(), name='resend-verify_email'),
    # path('email-verify/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),

    path('backend-signin/', views.AuthTokenAPIView.as_view(), name='auth-token'),
    path('social-signin/', views.SocialAuthTokenAPIView.as_view(), name='social-auth-token'),

    # path('password-reset/link/', views.LinkPasswordResetView.as_view(), name='password-reset-web'),
    path('password-reset/code/', views.CodePasswordResetView.as_view(), name='password-reset-mobile'),
    # path('password-reset/confirm/link/', views.LinkPasswordResetConfirmView.as_view(),
    #      name='password-reset-confirm-link'),
    path('password-reset/confirm/code/', views.CodePasswordResetConfirmView.as_view(),
         name='password-reset-confirm-code')
]
