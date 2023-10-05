from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('email-verify/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),

    path('backend-signin/', views.AuthTokenAPIView.as_view(), name='auth-token'),
    path('google-signin/', views.GoogleSignInAPIView.as_view(), name='google-signin'),
    path('facebook-signin/', views.FacebookSignInAPIView.as_view(), name='facebook-signin'),
    path('apple-signin/', views.AppleSignInAPIView.as_view(), name='apple-signin'),

    path('password-reset/link/', views.LinkPasswordResetView.as_view(), name='password-reset-web'),
    path('password-reset/code/', views.CodePasswordResetView.as_view(), name='password-reset-mobile'),
    path('password-reset/confirm/link/', views.LinkPasswordResetConfirmView.as_view(),
         name='password-reset-confirm-link'),
    path('password-reset/confirm/code/', views.CodePasswordResetConfirmView.as_view(),
         name='password-reset-confirm-code')
]
