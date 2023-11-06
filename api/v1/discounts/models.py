from django.db import models
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, FileExtensionValidator

from api.v1.tariffs.models import Tariff


class DiscountMixin(models.Model):
    discount_value = models.PositiveIntegerField(verbose_name='discount amount', validators=[MinValueValidator(1)])
    is_percent = models.BooleanField(default=True)

    def __str__(self):
        return str(self.discount_value) + ' %' if self.is_percent else ' SEK'

    def clean(self):
        if self.is_percent:
            if self.discount_value >= 100:
                raise ValidationError({'discount_value': 'Enter the percent value'})
        elif Tariff.objects.filter(price__lte=self.discount_value).exists():
            raise ValidationError({'discount_value': 'Enter the true value'})

    class Meta:
        abstract = True


class TariffDiscount(DiscountMixin):
    image = models.ImageField(upload_to='discounts/images/', max_length=500,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])])
    name = models.CharField(max_length=30)

    def clean(self):
        super().clean()
        if not self.pk and TariffDiscount.objects.exists():
            raise ValidationError('old discount object exists')

    class Meta:
        verbose_name_plural = 'Tariff Discount'


class TariffDiscountDetail(models.Model):
    tariff_discount = models.ForeignKey(TariffDiscount, on_delete=models.CASCADE)
    language = models.ForeignKey('languages.Language', on_delete=models.PROTECT)
    title = RichTextField(max_length=500)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ['tariff_discount', 'language']


class UserCodeDiscount(DiscountMixin):
    def clean(self):
        super().clean()
        if not self.pk and UserCodeDiscount.objects.exists():
            raise ValidationError('old student discount object exists')
