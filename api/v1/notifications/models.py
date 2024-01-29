from django.db import models
from django.utils.timezone import now


class Notification(models.Model):
    NOTIFICATION_TYPE = (
        (1, 'New Tariff'),
        (2, 'New Level'),
        (3, 'New Chapter'),
        (4, 'Report Response'),
        (5, 'Tariff Discount'),
    )
    NEW_TARIFF_TEXT = 'Yangi tariff sotib oldingiz. Amal qilish muddati: {expire_date}'
    NEW_LEVEL_TEXT = 'Yangi levelga o\'tdingiz. Level ID: {level_id}'
    NEW_CHAPTER_TEXT = '{n}-chi chapter ochildi. Oldingi chapterlarni muvaffaqiyatli tugatdingiz'
    REPORT_RESPONSE_TEXT = 'sizning jalobangiz korib chiqildi va javobi email addresingizga jonatildi'
    TARIFF_DISCOUNT_TEXT = 'biz barcha tarifflarga {discount_name} nomli chegirma e\'lon qildik'

    notification_type = models.PositiveSmallIntegerField(verbose_name='Type', choices=NOTIFICATION_TYPE)

    order = models.ForeignKey('payments.Order', on_delete=models.PROTECT, null=True)  # 1

    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, null=True)  # 2, 3

    chapter = models.ForeignKey('chapters.Chapter', on_delete=models.CASCADE, null=True)  # 3

    report = models.ForeignKey('reports.Report', on_delete=models.CASCADE, null=True)  # 4

    tariff_discount = models.ForeignKey('discounts.TariffDiscount', on_delete=models.CASCADE, null=True)  # 5

    desc = models.CharField(max_length=255, blank=True)  # 4 + to email
    is_viewed = models.BooleanField(default=False)
    viewed_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.notification_type == self.NOTIFICATION_TYPE[0][0]:  # 1
            self.desc = self.NEW_TARIFF_TEXT.format(expire_date=self.order.student.tariff_expire_date)
        elif self.notification_type == self.NOTIFICATION_TYPE[1][0]:  # 2
            self.desc = self.NEW_LEVEL_TEXT.format(level_id=self.student.level_id)
        elif self.notification_type == self.NOTIFICATION_TYPE[2][0]:  # 3
            self.desc = self.NEW_CHAPTER_TEXT.format(n=self.chapter_id)
        elif self.notification_type == self.NOTIFICATION_TYPE[3][0]:  # 4
            self.desc = self.REPORT_RESPONSE_TEXT
        elif self.notification_type == self.NOTIFICATION_TYPE[4][0]:  # 4
            self.desc = self.TARIFF_DISCOUNT_TEXT.format(discount_name=self.tariff_discount.name)

        if self.is_viewed and self.viewed_at is None:
            self.viewed_at = now()
        super().save(*args, **kwargs)

# class Swish
# class NewTariffDiscountNotification(models.Model):
