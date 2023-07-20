from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.payments.models import Order
from api.v1.discounts.models import StudentDiscount
from api.v1.accounts.models import CustomUser, StudentCalledEmail
from api.v1.tariffs.models import TariffDay


class StripeCheckoutSerializer(serializers.Serializer):
    tariff_id = serializers.IntegerField()
    user_code = serializers.CharField(required=False)

    def validate(self, attrs):
        student = self.context['request'].user
        user_code = attrs.get('user_code', '')
        tariff_id = attrs.get('tariff_id')

        try:
            tariff_day = TariffDay.objects.select_related('tariff').get(pk=tariff_id)
        except TariffDay.DoesNotExist:
            raise ValidationError({'tariff_id': ['not found']})

        if user_code:
            if user_code == student.user_code or not CustomUser.user_id_exists(user_code):
                raise ValidationError({'user_code': ['not found']})
            called_user = CustomUser.objects.get(user_code=user_code)
            obj, created = StudentCalledEmail.objects.get_or_create(email=called_user.email, student=student)
            if not created:
                raise ValidationError({'user_code': ['You have already registered this code']})

        if user_code:
            try:
                obj = StudentDiscount.objects.first()
                if not obj.is_active:
                    del attrs['user_code']
            except ValueError:
                del attrs['user_code']

        order = Order.objects.create(student_id=student.id, tariff_id=tariff_day.id, called_student_code=user_code)

        attrs['order'] = order
        attrs['tariff_day'] = tariff_day
        attrs['tariff'] = tariff_day.tariff
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['student', 'stripe_id', 'stripe_url']
