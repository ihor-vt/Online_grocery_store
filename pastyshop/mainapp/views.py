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


def custom_404(request, exception):
    """
    The custom_404 function is a custom 404 error handler.
    It takes two arguments: request and exception.
    The request argument is an HttpRequest object, which contains metadata about the requested page. The exception argument is an Exception object, which contains information about why the 404 error was triggered.
    
    :param request: Get the request object, which contains information about the current web request that has triggered this view
    :param exception: Pass the exception that was raised
    :return: The 404
    """
    return render(request, "mainapp/404.html")
