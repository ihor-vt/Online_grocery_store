import random
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from couponsapp.forms import CouponApplyForm
from shop.models import Product
from shop.recommender import Recommender
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    """
    The cart_add function is responsible for adding a product to the cart.
    It takes two arguments: request and product_id. The function first 
    creates an instance of Cart, passing it the current request object. 
    Then it gets the Product object with id equal to product_id or raises 
    404 if no such Product exists (using get_object_or_404). Next, we create
    an instance of CartAddProductForm and pass it POST data from the request;
    this will validate that data against our form definition in forms.py.
    
    :param request: Get the current cart
    :param product_id: Get the product from the database
    :return: An httpresponseredirect object, which redirects the user to the cart_detail view
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                quantity=cd['quantity'],
                override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    """
    The cart_remove function is a view that removes an item from the cart.
    It takes two arguments: request and product_id. The function first creates
    a Cart object, then gets the Product object with the given id or returns 404 
    if it doesn't exist. Finally, it calls remove() on this product.
    
    :param request: Access the current session
    :param product_id: Identify the product to be removed from the cart
    :return: A redirect to the cart_detail view
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    """
    The cart_detail function is responsible for displaying the contents of the cart.
    It also displays a form that allows users to apply coupons to their order, and it
    displays a list of recommended products based on what's in the user's cart.
    
    :param request: Get the current session
    :return: A dictionary with two keys: cart and coupon_apply_form
    """
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                                                            'quantity': item['quantity'],
                                                            'override': True})
    coupon_apply_form = CouponApplyForm()

    r = Recommender()
    cart_products = [item['product'] for item in cart]
    if(cart_products):
        recommended_products = r.suggest_products_for(
                                        cart_products,
                                        max_results=4)
    else:
        all_products = Product.objects.filter(available=True)
        recommended_products = random.sample(list(all_products), min(len(all_products), 4))
        
    return render(request, 'cart/detail.html', {'cart': cart,
                                                'coupon_apply_form': coupon_apply_form,
                                                'recommended_products': recommended_products})
