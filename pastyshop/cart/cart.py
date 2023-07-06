from decimal import Decimal
from django.conf import settings

from shop.models import Product
from couponsapp.models import Coupon


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # зберігаємо порожній словник в сесії користувача
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store current applied coupon
        self.coupon_id = self.session.get("coupon_id")

    def add(self, product, quantity=1, override_quantity=False):
        """
        The add function takes in a product object, and an optional quantity.
        If the product is already in the cart, it will update its quantity.
        Otherwise, it will add a new item to the cart.

        :param self: Access the object itself
        :param product: Add a product to the cart
        :param quantity: Set the quantity of a product in the cart
        :param override_quantity: Determine whether the quantity of a product in the cart should be updated or not
        :return: Nothing
        :doc-author: Ihor Voitiuk
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
            }
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def update(self, product, quantity):
        """
        The update function takes a product and quantity as arguments.
        It then converts the product id to a string, and checks if that string is in the cart dictionary.
        If it is, it updates the quantity of that item in the cart.

        :param self: Make the method work for every instance of a class
        :param product: Identify the product in the cart
        :param quantity: Update the quantity of a product in the cart
        :return: Nothing
        :doc-author: Ihor Voitiuk
        """
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] = quantity
            self.save()

    def remove(self, product):
        """
        The remove function takes a product and removes it from the cart.
            It does this by taking the product id, converting it to a string,
            and then deleting that key from the cart dictionary.

        :param self: Reference the object that is calling the method
        :param product: Remove the product from the cart
        :return: Nothing
        :doc-author: Ihor Voitiuk
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        The __iter__ function is a special function that allows you to iterate over the items in an object.
        In this case, we are using it to iterate over the items in our cart.
        The __iter__ function returns an iterator object which can be used by Python's
        for loops and other functions that expect an iterator.

        :param self: Access the attributes and methods of the class
        :return: An iterable object that can be looped over
        :doc-author: Ihor Voitiuk
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]["product"] = product
        for item in self.cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        The __len__ function is a special function that allows you to use the len()
            function on an object. For example, if you have a list of items in your cart,
            then calling len(cart) will return the number of items in your cart.

        :param self: Access the attributes and methods of the class
        :return: The total number of items in the cart
        :doc-author: Ihor Voitiuk
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """
        The get_total_price function returns the total price of all items in the cart.
        It does this by iterating over each item in self.cart, multiplying its quantity
        by its price, and adding that to a running total.

        :param self: Access the instance attributes and methods
        :return: The total price of the items in the cart
        :doc-author: Ihor Voitiuk
        """
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def clear(self):
        """
        The clear function deletes the cart from the user's session.
        It does this by deleting the CART_SESSION_ID key from self.session, and then setting self.session to modified.

        :param self: Represent the instance of the object itself
        :return: Nothing
        :doc-author: Ihor Voitiuk
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def save(self):
        """
        The save function saves the cart to the session.
        The session is a dictionary-like object that stores data on the server side.
        It allows us to store information about our users without having to create a database or save anything in files.

        :param self: Represent the instance of the object itself
        :return: Nothing
        :doc-author: Ihor Voitiuk
        """
        # зберігає корзину в сесії користувача
        self.session[settings.CART_SESSION_ID] = self.cart
        # позначаємо сесію як змінену
        self.session.modified = True

    @property
    def coupon(self):
        """
        The coupon function returns the coupon object associated with this order.
        If there is no coupon, it returns None.

        :param self: Represent the instance of the object itself
        :return: A coupon object if the coupon_id exists
        :doc-author: Ihor Voitiuk
        """
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        """
        The get_discount function returns the discount amount for a given order.
        It does this by checking if there is a coupon associated with the order, and
        if so, it calculates the discount based on that coupon's percentage value.
        If no coupon is associated with an order, then it simply returns 0.

        :param self: Refer to the current instance of the class
        :return: The discount amount
        :doc-author: Ihor Voitiuk
        """
        if self.coupon:
            return (
                self.coupon.discount / Decimal(100)
            ) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        """
        The get_total_price_after_discount function returns the total price of all
        products in the cart minus any discounts that may apply.

        :param self: Access the attributes and methods of the class
        :return: The total price after discount
        :doc-author: Ihor Voitiuk
        """
        return self.get_total_price() - self.get_discount()
