import stripe

from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.accounts.permissions import IsStudent

from .serializers import StripeCheckoutSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

default_image = 'https://media-ik.croma.com/prod/https://media.croma.com/image/upload/v1675775481/Croma%20Assets/' \
                'Small%20Appliances/Home%20Safety%20Security/Images/268787_mf0dot.png?tr=w-640'


class StripeCheckoutAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = StripeCheckoutSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        tariff_info = data['tariff_info']
        order = data['order']
        link_type = data['link_type']
        user = self.request.user

        if order.is_paid:
            return Response({'checkout_url': None, 'is_paid': order.is_paid}, status=status.HTTP_200_OK)

        product_data = {
            'name': tariff_info.title,
            'description': tariff_info.desc,
            'images': [
                default_image  # last
            ]
        }
        if not tariff_info.desc:
            del product_data['description']

        try:
            session_data = {
                'mode': 'payment',
                'payment_method_types': ['card'],
                'client_reference_id': order.id,
                'customer_email': user.email,
                'line_items': [],
                'discounts': [],
                'success_url': settings.PAYMENT_URLS[link_type]['success_url'],
                'cancel_url': settings.PAYMENT_URLS[link_type]['cancel_url']
            }
            session_data['line_items'].append({
                'price_data': {
                    'currency': 'SEK',
                    'unit_amount': order.tariff_price * 100,
                    'product_data': product_data
                },
                'quantity': 1
            })

            discount_title = ''
            discount_amount = 0

            if order.tariff_discount:
                discount_title += 'tariff'
                discount_amount += order.tariff_discount_amount

            if order.student_discount_amount > 0:
                discount_title += ', student discount'
                discount_amount += order.student_discount_amount

            if order.use_bonus_money and order.student_bonus_amount > 0:
                discount_title += ', bonus money'
                discount_amount += order.student_bonus_amount

            if discount_amount > 0:
                data = {
                    'name': discount_title,
                    'amount_off': discount_amount * 100,
                    'duration': 'once',
                    'currency': 'SEK'
                }

                stripe_coupon = stripe.Coupon.create(**data)
                session_data['discounts'].append({'coupon': stripe_coupon.id})

            checkout_session = stripe.checkout.Session.create(**session_data)
            order.payment_link = checkout_session.url
            order.save()
            return Response({'checkout_url': checkout_session.url, 'is_paid': order.is_paid}, status=status.HTTP_200_OK)
        except Exception as e:
            order.delete()  # last
            return Response(
                {'msg': 'something went wrong while creating stripe session', 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
