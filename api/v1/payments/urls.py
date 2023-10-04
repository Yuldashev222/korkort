from django.urls import path

from .views import OrderAPIView, CheckCouponAPIView
from .checkout import StripeCheckoutAPIView
from .webhooks import stripe_webhook_view  # , StripeWebhookView

urlpatterns = [
    path('stripe/create-checkout-session/', StripeCheckoutAPIView.as_view()),
    # path('stripe/webhooks/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('stripe/webhooks/', stripe_webhook_view, name='stripe-webhook'),
    path('orders/', OrderAPIView.as_view({'get': 'list'}), name='order-list'),
    path('check-coupon/', CheckCouponAPIView.as_view()),
    path('orders/<int:pk>/', OrderAPIView.as_view({'get': 'retrieve'}), name='order-detail'),
]
