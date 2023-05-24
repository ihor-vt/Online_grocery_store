from django.shortcuts import render

from shop.models import Product


def main_page(request):
    """
    The main_page function is the main page of the website. It displays a list
    of products that are available for purchase.

    :param request: Pass the request object to the view
    :return: The main
    """
    products = Product.objects.filter(available=True)[:4]

    return render(request, "mainapp/main.html", {"products": products})
