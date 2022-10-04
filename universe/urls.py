
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from universe.userapp.views import SignUpView
from universe.productapp import views as product_view
from . import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', product_view.marketPlace, name='index'),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'^accounts/signup/$', SignUpView.as_view(), name= "signup"),
    re_path(r'^userapp/', include('universe.userapp.urls')),
    re_path(r'^productapp/', include('universe.productapp.urls')),
    re_path(r'^paymentapp/', include('universe.paymentapp.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)