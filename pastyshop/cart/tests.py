from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.sessions.backends.db import SessionStore
from .cart import Cart
from .forms import CartAddProductForm

from authentication.models import CustomUser


class ProductStub:
    def __init__(self):
        self.name = None
        self.price = None

    def create(self, name, price):
        self.name = name
        self.price = price


class CartStub:
    def __init__(self):
        self.cart_items = []

    def add(self, product, quantity, override_quantity):
        cart_item = {
            "product": product,
            "quantity": quantity,
            "override_quantity": override_quantity,
        }
        self.cart_items.append(cart_item)

    def remove(self, product):
        self.cart_items = [
            item for item in self.cart_items if item["product"] != product
        ]

    def __len__(self):
        return len(self.cart_items)

    def __iter__(self):
        return iter(self.cart_items)


class SessionStoreStub:
    def __init__(self):
        self.session_data = {}


class CartTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            first_name="first_name",
            last_name="last_name",
            email="test@example.com",
            password="testpassword",
        )
        self.product = ProductStub()
        self.product.create(name="Test Product", price=10.0)

    def test_cart_add(self):
        cart = CartStub()
        initial_cart_count = len(cart)

        cart.add(product=self.product, quantity=2, override_quantity=False)

        self.assertEqual(len(cart), initial_cart_count + 1)
        self.assertTrue(any(item["product"] == self.product for item in cart))

    def test_cart_remove(self):
        cart = CartStub()
        cart.add(product=self.product, quantity=1, override_quantity=False)
        initial_cart_count = len(cart)

        cart.remove(self.product)

        self.assertEqual(len(cart), initial_cart_count - 1)
        self.assertFalse(any(item["product"] == self.product for item in cart))
