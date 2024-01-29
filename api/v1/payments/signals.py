from datetime import timedelta
from django.conf import settings
from django.dispatch import receiver
from django.utils.timezone import now
from django.db.models.signals import post_delete, post_save, pre_save

from api.v1.payments.tasks import change_student_tariff_expire_date
from api.v1.payments.models import Order
from api.v1.discounts.models import TariffDiscount, UserCodeDiscount
from api.v1.swish.models import CalledStudentAndSwishTransaction


@receiver(pre_save, sender=Order)
def check_order(instance, *args, **kwargs):
    tariff = instance.tariff
    student = instance.student
    called_student = instance.called_student

    if not instance.pk:
        instance.order_id = instance.generate_unique_order_id
        instance.student_email = student.email
        instance.student_name = student.name
        instance.student_user_code = student.user_code

        instance.tariff_price = tariff.price
        instance.tariff_days = tariff.days

        tariff_discount = TariffDiscount.objects.first()
        student_discount = UserCodeDiscount.objects.first()

        if tariff_discount:
            instance.tariff_discount_value = tariff_discount.discount_value
            instance.tariff_discount_name = tariff_discount.name
            instance.tariff_discount_is_percent = tariff_discount.is_percent
            if tariff_discount.is_percent:
                instance.tariff_discount_amount = round(instance.tariff_price * tariff_discount.discount_value / 100, 1)
            else:
                instance.tariff_discount_amount = tariff_discount.discount_value

        if instance.use_bonus_money:
            if student.bonus_money > 0:
                remaining_amount = instance.tariff_price - instance.tariff_discount_amount
                if remaining_amount > 0:
                    if student.bonus_money >= remaining_amount:
                        student.bonus_money -= remaining_amount
                        instance.student_bonus_amount = remaining_amount
                    else:
                        instance.student_bonus_amount = student.bonus_money
                        student.bonus_money = 0
                    student.save()

        elif called_student and student_discount:
            instance.called_student_name = called_student.name
            instance.called_student_email = called_student.email
            instance.called_student_code = called_student.user_code

            instance.user_code_discount_value = student_discount.discount_value
            instance.user_code_discount_is_percent = student_discount.is_percent
            if student_discount.is_percent:
                instance.user_code_discount_amount = round(
                    instance.tariff_price * student_discount.discount_value / 100, 1)
            else:
                instance.user_code_discount_amount = student_discount.discount_value

    all_discounts = instance.user_code_discount_amount + instance.tariff_discount_amount + instance.student_bonus_amount
    instance.purchased_price = instance.tariff_price - all_discounts
    if not instance.is_paid and instance.tariff_price <= all_discounts:
        instance.is_paid = True

    if instance.is_paid:
        if not instance.purchased_at:
            instance.purchased_at = now()

        if not instance.expire_at:
            last_order = Order.objects.filter(student_email=student.email, is_paid=True,
                                              expire_at__gt=instance.purchased_at.date()).order_by('expire_at').last()

            instance.expire_at = last_order.expire_at if last_order else instance.purchased_at.date()
            instance.expire_at += timedelta(days=instance.tariff_days)

        if not instance.called_student_bonus_added and instance.called_student:
            instance.called_student.bonus_money += round(instance.user_code_discount_amount, 1)
            instance.called_student.save()
            instance.called_student_bonus_added = True

        if instance.stripe_id and not instance.stripe_url:
            path = '/test/' if '_test_' in settings.STRIPE_SECRET_KEY else '/'
            instance.stripe_url = f'https://dashboard.stripe.com{path}payments/{instance.stripe_id}'


@receiver(post_save, sender=Order)
def change_student_tariff_expire_date_on_save(instance, *args, **kwargs):
    student = instance.student
    if instance.is_paid and instance.expire_at and student:
        change_student_tariff_expire_date(student.pk)

    if instance.is_paid and instance.called_student:
        CalledStudentAndSwishTransaction.objects.get_or_create(order_id=instance.pk)


@receiver(post_delete, sender=Order)
def reply_student_bonus_money(instance, *args, **kwargs):
    student = instance.student
    if not student:
        return

    if instance.is_paid:
        if instance.expire_at > now().date():
            change_student_tariff_expire_date(student.pk)

    elif instance.student_bonus_amount > 0:
        student.bonus_money += instance.student_bonus_amount
        student.save()
