import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views import View
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            # Invalid payload
            return HttpResponse(content=str(e), status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(content=str(e), status=400)

        if event.type == "checkout.session.completed":
            session = event.data.object
            if session.mode == 'payment' and session.payment_status == 'paid':
                try:
                    order = Order.objects.select_related('student').get(id=session.client_reference_id, is_paid=False)
                except Order.DoesNotExist as e:
                    return HttpResponse(content=str(e), status=400)
                order.is_paid = True
                order.stripe_id = session.payment_intent
                order.save()

                student = order.student
                message = render_to_string('payments/checkout.html')
                send_mail('Hello Everyone', message, settings.DEFAULT_FROM_EMAIL, recipient_list=[student.email],
                          html_message=message)

        return HttpResponse(status=200)
