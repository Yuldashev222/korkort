from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.general.enums import LINK_TYPES
from api.v1.tariffs.models import Tariff
from api.v1.payments.models import Order
from api.v1.accounts.models import CustomUser


class StripeCheckoutSerializer(serializers.Serializer):
    tariff_id = serializers.IntegerField()
    link_type = serializers.ChoiceField(choices=LINK_TYPES)
    use_bonus_money = serializers.BooleanField(default=False)
    user_code = serializers.CharField(required=False)

    def validate(self, attrs):
        called_student = None
        tariff_id = attrs.get('tariff_id')
        use_bonus_money = attrs.get('use_bonus_money')
        user_code = attrs.get('user_code', '')
        student = self.context['request'].user

        Order.delete_student_expire_orders()

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

        order = Order.objects.create(student=student, tariff=tariff, called_student=called_student,
                                     use_bonus_money=use_bonus_money)

        attrs['order'] = order
        attrs['tariff_info'] = tariff.tariff_info
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['student', 'stripe_id', 'stripe_url']
