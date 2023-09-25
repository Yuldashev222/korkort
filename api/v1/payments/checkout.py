import time
import stripe
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.accounts.permissions import IsStudent
from api.v1.payments.serializers import StripeCheckoutSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

default_image = 'https://media-ik.croma.com/prod/https://media.croma.com/image/upload/v1675775481/Croma%20Assets/' \
                'Small%20Appliances/Home%20Safety%20Security/Images/268787_mf0dot.png?tr=w-640'


class StripeCheckoutAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = StripeCheckoutSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tariff = serializer.validated_data['tariff']
        order = serializer.validated_data['order']

        if order.is_paid:
            return Response({'checkout_url': None, 'is_paid': True}, status=status.HTTP_200_OK)

        product_data = {
            'name': tariff.title,
            'images': [default_image]  # last
        }
        if tariff.desc:
            product_data['description'] = tariff.desc

        session_data = {
            'mode': 'payment',
            'payment_method_types': ['card'],
            'client_reference_id': order.id,
            'customer_email': self.request.user.email,
            'success_url': f'{settings.SUCCESS_PAYMENT_URL}?order_id={order.id}',
            'cancel_url': f'{settings.FAILURE_PAYMENT_URL}?order_id={order.id}',
            'expires_at': int(time.time()) + settings.STRIPE_CHECKOUT_TIMEOUT,
            'line_items': []
        }

        session_data['line_items'].append({
            'price_data': {
                'currency': settings.STRIPE_CHECKOUT_CURRENCY,
                'unit_amount': order.tariff_price * 100,
                'product_data': product_data
            },
            'quantity': 1
        })

        discount_title = ''
        discount_amount = 0

        if order.tariff_discount_amount > 0:
            discount_title += 'tariff'
            discount_amount += order.tariff_discount_amount

        if order.student_bonus_amount > 0:
            if discount_title:
                discount_title += ', '

            discount_title += 'bonus money'
            discount_amount += order.student_bonus_amount

        elif order.student_discount_amount > 0:
            if discount_title:
                discount_title += ', '
            discount_title += 'student discount'
            discount_amount += order.student_discount_amount

        if discount_amount > 0:
            data = {
                'name': discount_title,
                'amount_off': int(discount_amount * 100),
                'duration': 'once',
                'currency': settings.STRIPE_CHECKOUT_CURRENCY
            }

            stripe_coupon = stripe.Coupon.create(**data)
            session_data['discounts'] = [{'coupon': stripe_coupon.id}]

        try:
            checkout_session = stripe.checkout.Session.create(**session_data)
            order.payment_link = checkout_session.url
            order.save()
            return Response({'checkout_url': checkout_session.url, 'is_paid': False}, status=status.HTTP_200_OK)
        except Exception as e:
            order.delete()
            return Response(
                {'msg': 'something went wrong while creating stripe session', 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
