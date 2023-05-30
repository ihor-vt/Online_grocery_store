"""
URL configuration for pastyshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.conf.urls import handler404

# from mainapp import views

from paymentapp import webhooks


urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path(_("cart/"), include("cart.urls", namespace="cart")),
    path(_("orders/"), include("ordersapp.urls", namespace="orders")),
    path(_("payment/"), include("paymentapp.urls", namespace="payment")),
    path(_("coupons/"), include("couponsapp.urls", namespace="coupons")),
    path("users/", include("authentication.urls", namespace="users")),
    path("", include("mainapp.urls", namespace="main")),
    path("shop", include("shop.urls", namespace="shop")),
    path(_("contacts/"), include("contactsapp.urls", namespace="contacts")),
    path("rosetta/", include("rosetta.urls")),
)

urlpatterns += [
    path("payment/webhook/", webhooks.stripe_webhook, name="stripe-webhook"),
]

# handler404 = views.custom_404

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
