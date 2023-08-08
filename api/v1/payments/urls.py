from django.urls import path

from .checkout import StripeCheckoutAPIView
from .views import OrderAPIView
from .webhooks import StripeWebhookView

urlpatterns = [
    path('stripe/create-checkout-session/', StripeCheckoutAPIView.as_view()),
    path('stripe/webhooks/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('orders/', OrderAPIView.as_view({'get': 'list'}), name='order-list'),
    path('orders/<int:pk>/', OrderAPIView.as_view({'get': 'retrieve'}), name='order-detail'),
]
