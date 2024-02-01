from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from api.v1.tariffs.models import Tariff
from api.v1.payments.models import Order
from api.v1.accounts.models import CustomUser


class StripeCheckoutSerializer(serializers.Serializer):
    tariff_id = serializers.IntegerField()
    use_bonus_money = serializers.BooleanField(default=False)
    user_code = serializers.CharField(required=False, allow_null=True, min_length=6, max_length=6)

    def validate(self, attrs):
        called_student = None
        tariff_id = attrs['tariff_id']
        user_code = attrs.get('user_code')
        use_bonus_money = attrs['use_bonus_money']
        student = self.context['request'].user

        try:
            tariff = Tariff.objects.get(pk=tariff_id)
        except Tariff.DoesNotExist:
            raise ValidationError({'tariff_id': ['not found']})

        if user_code is not None:
            if use_bonus_money:
                raise ValidationError({'use_bonus_money': ['choice']})

            if user_code == student.user_code or not CustomUser.user_id_exists(user_code):
                raise ValidationError({'user_code': ['not found']})

            called_student = CustomUser.objects.get(user_code=user_code)
            if Order.objects.filter(called_student_email=called_student.email, student_email=student.email,
                                    is_paid=True).exists():
                raise PermissionDenied({'user_code': ['You have already registered this code']})

        elif user_code and student.bonus_money <= 0:
            raise ValidationError({'use_bonus_money': 'min limit'})

        order = Order.objects.create(student_id=student.pk, tariff_id=tariff.pk, called_student=called_student,
                                     use_bonus_money=use_bonus_money)

        attrs['order'] = order
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['student', 'stripe_id', 'stripe_url']


class CheckCouponSerializer(serializers.Serializer):
    user_code = serializers.CharField(max_length=6, min_length=6)

    def validate_user_code(self, value):
        student = self.context['request'].user

        if value == student.user_code or not CustomUser.user_id_exists(value):
            raise ValidationError('not valid')

        if Order.objects.filter(called_student__user_code=value, student_email=student.email, is_paid=True).exists():
            raise PermissionDenied('You have already registered this code')

        return value
