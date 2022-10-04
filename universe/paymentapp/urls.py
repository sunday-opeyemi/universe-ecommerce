from django.urls import re_path, path, include
from django.views.generic import TemplateView
from universe.paymentapp import views as payment_view

urlpatterns = [
    re_path('checkout/(?P<user_id>\d+)/', payment_view.checkoutFromCart , name='checkout'),
    re_path('payment_success/(?P<invoice_id>\d+)/', payment_view.paymentSuccess , name='payment_success'),
    re_path('payment_fails/(?P<invoice_id>\d+)/', payment_view.paymentFail , name='payment_fails'),
    re_path('track_order/(?P<user_id>\d+)/', payment_view.trackOrder , name='track_order'),
    re_path('product_invoice/(?P<invoice_id>\d+)/', payment_view.productInvoice , name='product_invoice'),
    re_path('deliver_product/(?P<invoice_id>\d+)/', payment_view.productDelivered , name='deliver_product'),

]