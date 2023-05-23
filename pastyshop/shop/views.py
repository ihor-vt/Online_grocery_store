from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .models import Category, Product
from .recommender import Recommender
from cart.forms import CartAddProductForm
from .forms import ProductFilterForm, SearchForm


def product_list(request, category_slug=None):
    filter_form = ProductFilterForm(request.GET)
    orderby = None  # Assign a default value to orderby

    if filter_form.is_valid():
        orderby = filter_form.cleaned_data["orderby"]

    category = None
    categories = Category.objects.all()
    all_products = Product.objects.filter(available=True)

    # Apply sorting based on the selected option
    if orderby:
        all_products = filter_form.apply_sorting(all_products)

    total_products_count = all_products.count()

    # Pagination with 2 products per page
    paginator = Paginator(all_products, 20)
    page_number = request.GET.get("page", 1)
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer, deliver the first page
        products = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range, deliver the last page of results
        products = paginator.page(paginator.num_pages)

    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(
            Category,
            translations__language_code=language,
            translations__slug=category_slug,
        )
        products = all_products.filter(category=category)
        total_products_count = products.count()

    return render(
        request,
        "shop/product/list.html",
        {
            "category": category,
            "categories": categories,
            "products": products,
            "filter_form": filter_form,
            "total_products_count": total_products_count,
        },
    )


def product_detail(request, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(
        Product,
        id=id,
        translations__language_code=language,
        translations__slug=slug,
        available=True,
    )
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    return render(
        request,
        "shop/product/detail.html",
        {
            "product": product,
            "cart_product_form": cart_product_form,
            "recommended_products": recommended_products,
        },
    )


def products_search(request):
    form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            search_vector = (
                SearchVector("translations__name", weight="A")
                + SearchVector("translations__description", weight="B")
                + SearchVector("translations__mini_description", weight="B")
            )
            search_query = SearchQuery(query)

            products = Product.objects.filter(available=True)

            results = (
                products.annotate(
                    search=search_vector, rank=SearchRank(search_vector, search_query)
                )
                .filter(search=search_query)
                .order_by("-updated")
            )

    return render(
        request,
        "shop/product/search.html",
        {"form": form, "query": query, "results": results},
    )
