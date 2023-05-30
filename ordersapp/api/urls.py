from django.urls import include, path
from rest_framework import routers

from ordersapp.api.views import OrderViewSet, OrderItemViewSet


app_name = "orders_api"

router = routers.DefaultRouter()
router.register(r"orders", OrderViewSet)
router.register(r"order-items", OrderItemViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
