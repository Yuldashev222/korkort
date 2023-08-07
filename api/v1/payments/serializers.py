from datetime import timedelta

from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.payments.models import Order
from api.v1.accounts.models import CustomUser
from api.v1.tariffs.models import Tariff


class StripeCheckoutSerializer(serializers.Serializer):
    tariff_id = serializers.IntegerField()
    use_bonus_money = serializers.BooleanField(default=False)
    user_code = serializers.CharField(required=False)

    def validate(self, attrs):
        called_student = None
        tariff_id = attrs.get('tariff_id')
        use_bonus_money = attrs.get('use_bonus_money')
        user_code = attrs.get('user_code', '')
        student = self.context['request'].user

        # last
        Order.objects.filter(student=student, is_paid=False, created_at__gt=now() - timedelta(minutes=10)).delete()

        try:
            tariff = Tariff.objects.select_related('tariff_info').get(pk=tariff_id)
        except Tariff.DoesNotExist:
            raise ValidationError({'tariff_id': ['not found']})

        if user_code:
            if not tariff.student_discount:
                raise ValidationError({'user_code': ['Currently, the coupon system is not working for this tariff']})
            if user_code == student.user_code or not CustomUser.user_id_exists(user_code):
                raise ValidationError({'user_code': ['not found']})
            called_student = CustomUser.objects.get(user_code=user_code)
            if Order.objects.filter(called_student_email=called_student.email, student=student).exists():
                raise ValidationError({'user_code': ['You have already registered this code']})

        order = Order.objects.create(student=student, tariff=tariff, called_student=called_student)

        if use_bonus_money and student.bonus_money:
            remaining_amount = order.tariff_price - (order.student_discount_amount + order.tariff_discount_amount)
            if remaining_amount > 0:
                if student.bonus_money >= remaining_amount:
                    student.bonus_money -= remaining_amount
                    order.student_bonus_amount = remaining_amount
                else:
                    order.student_bonus_amount = student.bonus_money
                    student.bonus_money = 0
                student.save()
                order.save()

        attrs['order'] = order
        attrs['tariff_info'] = tariff.tariff_info
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['student', 'stripe_id', 'stripe_url']
