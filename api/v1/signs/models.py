from django.core.validators import FileExtensionValidator
from django.db import models

#
# class FirstModel(models.Model):
#     image = models.ImageField(upload_to='signs/images/', max_length=300,
#                               validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])])
#     title = models.CharField(max_length=300)
#
#
# class SecondModel(FirstModel):
#     pass
