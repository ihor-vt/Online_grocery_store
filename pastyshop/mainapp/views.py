from django.shortcuts import redirect, render

from shop.models import Product

# Create your views here.
def main_page(request):
    products = Product.objects.filter(available=True)[:4]

    return render(request, 'mainapp/main.html', {"products": products})