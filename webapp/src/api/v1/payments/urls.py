from django.urls import path

from .views import StripeCheckoutAPIView, StripeWebhookView

urlpatterns = [
    path('stripe/create-checkout-session/', StripeCheckoutAPIView.as_view()),
    path('stripe/webhooks/', StripeWebhookView.as_view(), name='stripe-webhook')
]
