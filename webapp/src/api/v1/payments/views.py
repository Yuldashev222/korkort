import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views import View
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt

from api.v1.accounts.models import CustomUser

from .serializers import StripeCheckoutSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY_TEST


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError:
            # Invalid signature
            return HttpResponse(status=400)

        if event["type"] == "checkout.session.completed":
            email = event['data']['object']['customer_email']
            user = CustomUser.objects.get(email=email)

            message = render_to_string('payments/checkout.html')

            send_mail('', message, settings.DEFAULT_FROM_EMAIL, recipient_list=[email], html_message=message)

        return HttpResponse(status=200)


class StripeCheckoutAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StripeCheckoutSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tariff = serializer.validated_data['tariff']
        product_data = {
            'name': tariff.title,
            'description': tariff.desc,
            'images': [
                # f'{request.build_absolute_uri(tariff.image.url)}'
            ]
        }
        if not tariff.desc:
            del product_data['description']
        try:
            user = self.request.user
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'SEK',
                            'unit_amount': (tariff.price - tariff.discount_price) * 100,
                            'product_data': product_data
                        },
                        'quantity': 1
                    },
                ],
                customer_email=user.email,
                payment_method_types=['card'],
                metadata={'product_id': tariff.id},
                mode='payment',
                success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/?success=false',
            )

            return redirect(checkout_session.url)
        except Exception as e:
            return Response(
                {'msg': 'something went wrong while creating stripe session', 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
