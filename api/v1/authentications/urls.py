from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('email-verify/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),

    path('backend-signin/', views.AuthTokenAPIView.as_view(), name='auth-token'),
    path('google-signin/android/', views.GoogleSignInAPIView.as_view(), name='google-signin'),
    path('google-signin/web/', views.GoogleSignInAPIView.as_view(), name='google-signin'),
    path('facebook-signin/', views.FacebookSignInAPIView.as_view(), name='facebook-signin'),

    path('password-reset/', views.PasswordResetView.as_view(), name='password-reset'),
    path('password-reset/confirm/<str:uidb64>/<str:token>/', views.PasswordResetConfirmView.as_view(),
         name='password-reset-confirm')
]
