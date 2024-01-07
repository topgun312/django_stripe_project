from django.urls import path

from payments.views import (
    CancelView,
    CreateCheckoutSessionView,
    ItemsList,
    ItemView,
    SuccessView,
    stripe_config,
)

urlpatterns = [
    path('', ItemsList.as_view(), name='items_list'),
    path("buy/<int:item_id>/", CreateCheckoutSessionView.as_view(), name='checkout_session'),
    path('item/<int:item_id>/', ItemView.as_view(), name='item'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('config/', stripe_config, name='config'),
]

