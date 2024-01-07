from django.contrib import admin

from payments.models import Discount, Item, Order, OrderItem, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
  list_display = ['name', 'description', 'price', 'currency']
  fields = ['name', 'description', 'price']
  ordering = ('-price',)
  list_per_page = 5


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
  list_display = ['display_name', 'percentage', 'inclusive']
  fields = ['display_name', 'percentage', 'inclusive']
  ordering = ('-percentage',)
  list_per_page = 5


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
  list_display = ['name', 'percent_off', 'duration']
  fields = ['name', 'percent_off', 'duration']
  ordering = ('-percent_off',)
  list_per_page = 5


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ['buyer', 'item', 'tax', 'discount']
  fields = ['buyer', 'item', 'tax', 'discount']
  ordering = ('-item',)
  list_per_page = 5


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
  list_display = ['item', 'order', 'price', 'quantity']
  fields = ['item', 'order', 'price', 'quantity']
  ordering = ('-order',)
  list_per_page = 5


