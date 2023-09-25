from django.db import models
from ckeditor.fields import RichTextField
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class DiscountMixin(models.Model):
    title = RichTextField(max_length=200, blank=True)
    discount_value = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_percent = models.BooleanField(default=True)

    def clean(self):
        if self.is_percent and self.discount_value > 100:
            raise ValidationError({'discount_value': 'Enter the percent value'})

    def __str__(self):
        if self.is_percent:
            return f'{self.title}: {self.discount_value} %'[:30]
        return f'{self.title}: {self.discount_value} SEK'[:30]

    class Meta:
        abstract = True


class TariffDiscount(DiscountMixin):
    image = models.ImageField(upload_to='discounts/images/', max_length=300)

    @classmethod
    def get_tariff_discount(cls):
        tariff_discount = cache.get('tariff_discount')
        if not tariff_discount:
            cls.set_redis()
            tariff_discount = cache.get('tariff_discount')
        return tariff_discount

    @classmethod
    def set_redis(cls):
        obj = cls.objects.first()
        if obj:
            cache.set('tariff_discount', {'is_percent': obj.is_percent,
                                          'discount_value': obj.discount_value,
                                          'title': obj.title,
                                          'image_url': obj.image.url},
                      60 * 60 * 24 * 30
                      )

        elif cache.get('tariff_discount'):
            cache.delete('tariff_discount')

    def clean(self):
        if not self.pk and TariffDiscount.objects.exists():
            raise ValidationError('old discount object exists')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['discount_value', 'is_percent'], name='unique discounts')]


class StudentDiscount(DiscountMixin):
    def clean(self):
        if not self.pk and StudentDiscount.objects.exists():
            raise ValidationError('old student discount object exists')

    @classmethod
    def get_student_discount(cls):
        student_discount = cache.get('student_discount')
        if not student_discount:
            cls.set_redis()
            student_discount = cache.get('student_discount')
        return student_discount

    @classmethod
    def set_redis(cls):
        obj = cls.objects.first()
        if obj:
            cache.set('student_discount', {'is_percent': obj.is_percent,
                                           'discount_value': obj.discount_value},
                      60 * 60 * 24 * 30)

        elif cache.get('student_discount'):
            cache.delete('student_discount')
