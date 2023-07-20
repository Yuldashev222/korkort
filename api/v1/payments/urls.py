from django.urls import path

from .checkout_test import StripeCheckoutAPIView, success_view, cancel_view
from .views import OrderAPIView
from .webhooks import StripeWebhookView

urlpatterns = [
    path('stripe/create-checkout-session/', StripeCheckoutAPIView.as_view()),
    path('stripe/webhooks/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('orders/', OrderAPIView.as_view({'get': 'list'}), name='order-list'),
    path('orders/<int:pk>/', OrderAPIView.as_view({'get': 'retrieve'}), name='order-detail'),

    path('success/', success_view, name='success-view'),
    path('cancel/', cancel_view, name='cancel-view')
]
