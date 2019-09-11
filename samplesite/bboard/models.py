import uuid

from django.db import models
from django.core import validators
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

def validate_even(val):
        if val % 2 != 0:
            raise ValidationError('Число % (value)s нечетное', code='odd',
                                  params={
                                      'value': val
                                  })

class Bb(models.Model):
    title = models.CharField(max_length=50,
        validators=[validators.RegexValidator(regex='^.{4,}$')],
        verbose_name='Товар', unique_for_date='published')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена',
                                validators=[validate_even])
    published = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric',
                               on_delete=models.PROTECT,
                               verbose_name='Рубрика', 
                               related_query_name='entry')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
                          editable=False)

    


    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Укажите описание ' +
                                                 'продаваемого товара')
        if self.price and self.price < 0:
            errors['price'] = ValidationError('Укажите ' +
                                               'неотрицательное значение \
                                                цены')
        if errors:
            raise ValidationError(errors)
        errors[NON_FIELD_ERRORS] = ValidationError('Ошибка в модели!')

    def title_and_price(self):
        if self.price:
            return '%s (%.2f)' % (self.title, self.price)
        else:
            return self.title
    title_and_price.short_description = 'Название и цена'

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published']
        # order_with_respect_to = 'rubric'
        unique_together = (('title', 'published'),
                           ('title', 'price', 'rubric'),
                          )


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')
    # rubric = models.ForeignKey('rubrics.Rubric', on_delete=models.PROTECT)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']


class AdvUser(models.Model):
    
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Spare(models.Model):
    
     name = models.CharField(max_length=30)

class Machine(models.Model):
    
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare)
    
    
class MinMaxValueValidator:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value
        
    def __call__(self, val):
        if val < self.min_value or val > self.max_value:
            raise ValidationError('Введенное число должно ' +
                                  'находиться в диапазоне от % (min)s до \
                                      % (max)s', code='out_of_range',
                                      params={'min': self.min_value, 
                                              'max': self.max_value})