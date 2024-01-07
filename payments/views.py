import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, TemplateView
from stripe.api_resources.checkout import Session
from payments.models import Item, Order


@csrf_exempt
def stripe_config(request):
  """
  Представление для получения публичного Stripe KEY
  """
  if request.method == 'GET':
    stripe_config = {'publicKey': settings.STRIPE_PUBLIC_KEY}
    return JsonResponse(stripe_config, safe=False)


class ItemsList(ListView):
  """
  Представление для получения публичного списка товаров
  """
  model = Item
  template_name = 'payments/items_list.html'
  context_object_name = 'items'


class ItemView(DetailView):
  """
  Представление для получения детальной страницы товара
  """
  model = Item
  template_name = 'payments/item.html'
  context_object_name = 'item'
  pk_url_kwarg = 'item_id'


class CreateCheckoutSessionView(View):
  """
  Представление для оформления нового сеанса оформления заказа и создания платежа Stripe
  """
  def get(self, request, *args, **kwargs):
    item_id = self.kwargs['item_id']
    item = Item.objects.get(id=item_id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    discounts = []
    order = Order.objects.filter(item=item.pk).select_related('tax', 'discount', 'item').first()
    if order.discount:
      coupon = stripe.Coupon.create(name=order.discount.name,
                                    percent_off=order.discount.percent_off,
                                    duration=order.discount.duration)
      discounts = [{'coupon': f"{coupon.id}"}]
    tax = stripe.TaxRate.create(display_name=order.tax.display_name,
                                percentage=order.tax.percentage,
                                inclusive=order.tax.inclusive)
    YOUR_DOMAIN = 'http://localhost:8000/'
    ACTUAL_DOMAIN = 'http://130.193.52.110:8000/'
    if settings.DEBUG:
      domain = YOUR_DOMAIN
    else:
      domain = ACTUAL_DOMAIN
    try:
      checkout_session = Session.create(
        payment_method_types=['card'],
        mode='payment',
          line_items=[{"price_data": {"product_data": {"name": item.name},
                                      "currency": item.currency,
                                      "unit_amount": int(item.price * 100)},
                       "quantity": order.items.values()[0].get('quantity'),
                      "tax_rates": [tax['id']]
          }],
        metadata={'product_id': item.id},
        discounts=discounts,
        success_url=f"{domain}/success/",
        cancel_url=f"{domain}/cancel/"
      )
      return JsonResponse({'sessionId': checkout_session['id']})
    except Exception as ex:
      return JsonResponse({'error': str(ex)})


class SuccessView(TemplateView):
  """
  Представление для перенаправления в случае успешного оформления платежа
  """
  template_name = 'payments/success.html'


class CancelView(TemplateView):
  """
  Представление для перенаправления в случае отмены оформления платежа
  """
  template_name = 'payments/cancel.html'