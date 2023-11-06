import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            return HttpResponse(str(e), status=400)

        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(str(e), status=400)

        # Handle the event
        if event['type'] == 'checkout.session.completed':
            print('================================================')
            # session = event['data']['object']
            # if session.mode == 'payment' and session.payment_status == 'paid':
            #     try:
            #         order = Order.objects.select_related('student').get(pk=session.client_reference_id, is_paid=False)
            #     except Order.DoesNotExist as e:
            #         return HttpResponse(content=str(e), status=404)
            #     order.is_paid = True
            #     order.stripe_id = session.payment_intent
            #     order.save()
            #
            #     student = order.student
            #     message = render_to_string('payments/checkout.html')
            #     send_mail(subject='Hello Everyone', message=message, from_email=None, recipient_list=[student.email],
            #               html_message=message)

        return HttpResponse(status=200)
