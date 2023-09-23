from datetime import timedelta
from django.conf import settings
from django.dispatch import receiver
from django.db.models import Max
from django.utils.timezone import now
from django.db.models.signals import post_delete, post_save, pre_save
 
from api.v1.payments.tasks import change_student_tariff_expire_date
from api.v1.payments.models import Order
from api.v1.discounts.models import TariffDiscount, StudentDiscount


@receiver(post_delete, sender=Order)
def reply_student_bonus_money(instance, *args, **kwargs):
    student = instance.student
    now_datetime = now()
    if student:
        if instance.is_paid:
            max_expire_at = Order.objects.filter(student=student, is_paid=True, expire_at__gt=now_datetime
                                                 ).aggregate(max_expire_at=Max('expire_at'))['max_expire_at']
            if max_expire_at:
                student.tariff_expire_date = max_expire_at
            else:
                student.tariff_expire_date = now_datetime
            student.save()

        elif instance.student_bonus_amount:
            student.bonus_money += instance.student_bonus_amount
            student.save()


@receiver(post_save, sender=Order)
def change_student_tariff_expire_date_on_save(instance, *args, **kwargs):
    if instance.student and instance.is_paid and instance.expire_at > instance.student.tariff_expire_date:
        change_student_tariff_expire_date.delay(instance.student_id)


@receiver(pre_save, sender=Order)
def check_order(instance, *args, **kwargs):
    tariff = instance.tariff
    student = instance.student
    called_student = instance.called_student

    if not instance.pk:
        instance.order_id = instance.generate_unique_order_id
        instance.student_email = student.email

        instance.tariff_title = tariff.title
        instance.tariff_price = tariff.price
        instance.tariff_days = tariff.days

        if tariff.tariff_discount:

            tariff_discount = TariffDiscount.get_tariff_discount()

            if tariff_discount:
                instance.tariff_discount_value = tariff_discount['discount_value']
                instance.tariff_discount_title = tariff_discount['title']
                instance.tariff_discount_is_percent = tariff_discount['is_percent']
                instance.tariff_discount_amount = tariff.tariff_discount_amount

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

        elif tariff.student_discount and called_student:
            instance.called_student_code = called_student.user_code
            instance.called_student_email = called_student.email

            student_discount = StudentDiscount.get_student_discount()
            if student_discount:
                instance.student_discount_value = student_discount['discount_value']
                instance.student_discount_is_percent = student_discount['is_percent']
                instance.student_discount_amount = tariff.student_discount_amount

    all_discounts = instance.student_discount_amount + instance.tariff_discount_amount + instance.student_bonus_amount
    instance.purchased_price = instance.tariff_price - all_discounts
    if not instance.is_paid and instance.tariff_price <= all_discounts:
        instance.is_paid = True

    if instance.is_paid:
        if not instance.purchased_at:
            instance.purchased_at = now()

        if not instance.expire_at:
            max_expire_at = Order.objects.exclude(id=instance.pk).filter(
                student=student, is_paid=True, expire_at__gt=instance.purchased_at
            ).aggregate(max_expire_at=Max('expire_at'))['max_expire_at']

            max_expire_at = max_expire_at if max_expire_at else instance.purchased_at
            instance.expire_at = max_expire_at + timedelta(days=instance.tariff_days)

        if called_student and not instance.called_student_bonus_added:
            called_student.bonus_money += round(instance.student_discount_amount, 1)
            called_student.save()
            instance.called_student_bonus_added = True

        if instance.stripe_id and not instance.stripe_url:
            path = '/test/' if '_test_' in settings.STRIPE_SECRET_KEY else '/'
            instance.stripe_url = f'https://dashboard.stripe.com{path}payments/{instance.stripe_id}'
