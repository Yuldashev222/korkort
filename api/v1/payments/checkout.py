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
        tariff = data['tariff']
        tariff_day = data['tariff_day']
        order = data['order']
        user = self.request.user

        if order.is_paid:
            return Response({'checkout_url': None, 'is_paid': True}, status=status.HTTP_200_OK)

        product_data = {
            'name': tariff.title,
            'description': tariff.desc,
            'images': [
                default_image  # last
            ]
        }
        if not tariff.desc:
            del product_data['description']

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'SEK',
                            'unit_amount': order.purchased_price * 100,
                            'product_data': product_data
                        },
                        'quantity': 1
                    },
                ],
                client_reference_id=order.id,
                customer_email=user.email,
                payment_method_types=['card'],
                metadata={'product_id': tariff_day.id},
                mode='payment',
                success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/?success=false',
            )
            return Response({'checkout_url': checkout_session.url, 'is_paid': False}, status=status.HTTP_200_OK)
        except Exception as e:
            order.delete()  # last
            return Response(
                {'msg': 'something went wrong while creating stripe session', 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
