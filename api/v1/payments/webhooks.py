import json
import stripe
from config import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
 

from api.v1.payments.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = 'whsec_e9092e9da384c906358bb1684aee480f059eba910ba30f13c11d4f97604994b0'


# Using Django
@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body

    try:
        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

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
