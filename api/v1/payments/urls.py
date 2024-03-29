from django.urls import path

from .views import OrderAPIView, CheckCouponAPIView
from .checkout import StripeCheckoutAPIView
from .webhooks import StripeWebhookView

urlpatterns = [
    path('stripe/create-checkout-session/', StripeCheckoutAPIView.as_view()),
    path('stripe/webhooks/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('check-coupon/', CheckCouponAPIView.as_view()),

    path('orders/', OrderAPIView.as_view({'get': 'list'}), name='order-list'),
    path('orders/<int:pk>/', OrderAPIView.as_view({'get': 'retrieve'}), name='order-detail'),
]
