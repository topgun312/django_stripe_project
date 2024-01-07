from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Item(models.Model):
  """
  Модель Item для продаваемых товаров
  """
  class Currency(models.TextChoices):
    USD = "usd", "usd"
    EUR = "eur", "eur"

  name = models.CharField(max_length=255, verbose_name='Товар')
  description = models.TextField(max_length=1000, blank=True, verbose_name='Описание товара')
  price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
  currency = models.CharField(max_length=5, default=Currency.USD, choices=Currency.choices)

  class Meta:
    verbose_name = 'Товар'
    verbose_name_plural = 'Товары'

  def __str__(self):
    return self.name


class Order(models.Model):
  """
  Модель Order для заказа товара
  """
  buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
  item = models.ForeignKey('Item', on_delete=models.PROTECT, related_name='orders')
  tax = models.ForeignKey('Tax', on_delete=models.PROTECT, null=True, related_name='orders', verbose_name='Налог')
  discount = models.ForeignKey('Discount', on_delete=models.PROTECT, null=True, related_name='orders', verbose_name='Скидка')
  created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания заказа')

  objects = models.Manager()
  class Meta:
    verbose_name = 'Заказ'
    verbose_name_plural = 'Заказы'

  def __str__(self):
    return f'Заказ {self.item.name}'

  def get_total_cost(self):
    return sum(item.get_cost() for item in self.items.all())


class Discount(models.Model):
  """
  Модель Discount, скидки для продаваемых товаров
  """
  class Duration(models.TextChoices):
    FOREVER = "forever", "forever"
    ONCE = "once", "once"
    REPEATING = "repeating", "repeating"
  name = models.CharField(max_length=255, unique=True, verbose_name='Купон')
  percent_off = models.IntegerField(validators=[MinValueValidator(1, message='Минимум 1 процент'),
                                                MaxValueValidator(100, message='Максимум 100 процентов')], verbose_name='Процент скидки')
  duration = models.CharField(max_length=10, default=Duration.ONCE, choices=Duration.choices, verbose_name='Продолжительность')

  class Meta:
    verbose_name = 'Скидка'
    verbose_name_plural = 'Скидки'

  def __str__(self):
    return self.name

  def get_discount(self):
    return self.percent_off

class Tax(models.Model):
  """
  Модель Tax, налоги для продаваемых товаров
  """
  class TaxTypes(models.TextChoices):
    VAT = "VAT", "VAT Tax"
    SALE = "SALE", "Sales Tax"
    GST = "GST", "GST Tax"
  display_name = models.CharField(max_length=10, default=TaxTypes.VAT, choices=TaxTypes.choices, verbose_name='Тип налогооблажения')
  percentage = models.DecimalField(decimal_places=4, max_digits=8, verbose_name='Процент налога')
  inclusive = models.BooleanField(default=False, verbose_name='Налог включен')

  class Meta:
    verbose_name = 'Налог'
    verbose_name_plural = 'Налоги'

  def __str__(self):
    return self.display_name

  def get_tax(self):
    return self.percentage


class OrderItem(models.Model):
  """
  Модель OrderItem для взаимодействия товаров и заказов
  """
  order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
  item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='order_items')
  price = models.DecimalField(max_digits=10, decimal_places=2)
  quantity = models.PositiveIntegerField(default=1, blank=False)

  class Meta:
    verbose_name = 'Заказ товара'
    verbose_name_plural = 'Заказ товаров'

  def __str__(self):
    return self.item.__str__()

  def get_cost(self):
    return self.price * self.quantity
