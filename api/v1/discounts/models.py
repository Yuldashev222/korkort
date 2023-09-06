from django.db import models
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class DiscountMixin(models.Model):
    title = models.CharField(max_length=200, blank=True)
    discount_value = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_percent = models.BooleanField(default=True)

    def clean(self):
        if self.is_percent and self.discount_value > 100:
            raise ValidationError({'discount_value': 'Enter the percent value'})

    def __str__(self):
        if self.is_percent:
            return f'{self.title}: {self.discount_value} %'
        return f'{self.title}: {self.discount_value} SEK'

    class Meta:
        abstract = True


class TariffDiscount(DiscountMixin):
    # valid_from = models.DateField()
    # valid_to = models.DateField()
    image = models.ImageField(upload_to='discounts/images/')

    @classmethod
    def set_redis(cls):
        obj = cls.objects.first()
        if obj:
            cache.set('tariff_discount',
                      {
                          'is_percent': obj.is_percent,
                          'discount_value': obj.discount_value,
                          'title': obj.title,
                          # 'valid_from': obj.valid_from,
                          # 'valid_to': obj.valid_to,
                          'image_url': obj.image.url,
                      },
                      60 * 60 * 24 * 30
                      )

        elif cache.get('tariff_discount'):
            cache.delete('tariff_discount')

    def clean(self):
        if not self.pk and TariffDiscount.objects.exists():
            raise ValidationError('old discount object exists')

        # if self.valid_from >= self.valid_to:
            # raise ValidationError({'valid_from': 'the start time must be less than the end time.'})

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['discount_value', 'is_percent'], name='unique discounts')
        ]


class StudentDiscount(DiscountMixin):
    def clean(self):
        if not self.pk and StudentDiscount.objects.exists():
            raise ValidationError('old student discount object exists')

    @classmethod
    def set_redis(cls):
        obj = cls.objects.first()
        if obj:
            cache.set('student_discount',
                      {'is_percent': obj.is_percent, 'discount_value': obj.discount_value}, 60 * 60 * 24 * 30)

        elif cache.get('student_discount'):
            cache.delete('student_discount')
