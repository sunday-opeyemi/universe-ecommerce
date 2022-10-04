from django.urls import re_path
from django.views.generic import TemplateView
from universe.productapp import views as product_view

urlpatterns = [
    
    re_path('upload_product', product_view.uploadProduct , name='upload_product'),
    re_path('display_product', product_view.displayProduct , name='display_product'), 
    re_path('approve_product/(?P<product_id>\d+)/', product_view.approveProduct , name='approve_product'),
    re_path('edit_product/(?P<product_id>\d+)/', product_view.editProduct , name='edit_product'),
    re_path('more_product/(?P<category>\w+)/', product_view.moreProduct , name='more_product'),
    re_path('product_details/(?P<product_id>\d+)/', product_view.productDetails , name='product_details'),
    re_path('edit_cart/(?P<product_id>\d+)/', product_view.editMyCart , name='edit_cart'),
    re_path('remove_from_cart/(?P<product_id>\d+)/', product_view.removeFromCart , name='remove_from_cart'),
    re_path('view_mycart/(?P<user_id>\d+)/', product_view.viewMyCart , name='view_mycart'),

]
