import random

from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .models import Category, Product, Comment
from .recommender import Recommender
from cart.forms import CartAddProductForm
from .forms import ProductFilterForm, SearchForm, CommentForm


def product_list(request, category_slug=None):
    """
    The product_list function is responsible for displaying a list of products.
    It can be filtered by category and sorted by price, name or popularity.
    The function accepts an optional parameter called category_slug that allows
    us to filter the product list by a specific category.

    :param request: Get the current request
    :param category_slug: Filter the products by category
    :return: A rendered template, which is then displayed to the user
    """
    filter_form = ProductFilterForm(request.GET)
    orderby = None  # Assign a default value to orderby

    if filter_form.is_valid():
        orderby = filter_form.cleaned_data["orderby"]

    category = None
    categories = Category.objects.all()
    all_products = Product.objects.filter(available=True).order_by('?').distinct()

    # Apply sorting based on the selected option
    if orderby:
        all_products = filter_form.apply_sorting(all_products)

    total_products_count = all_products.count()

    # Pagination with 2 products per page
    paginator = Paginator(all_products, 9)
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
    """
    The product_detail function is responsible for displaying a single product.
    It takes the id and slug of the product as arguments, fetches it from the database,
    and passes it to a template along with an add-to-cart form. It also uses Recommender to fetch recommended products.

    :param request: Get the current request
    :param id: Get the product from the database
    :param slug: Get the product from the database
    :return: A response with the rendered product/detail
    """

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
    if recommended_products.count == 0:
        all_products = Product.objects.filter(available=True)
        recommended_products = random.sample(list(all_products), min(len(all_products), 5))

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = None
            comment = comment_form.save(commit=False)
            comment.product = product
            comment.save()
    comment_form = CommentForm()

    # comments = Comment.objects.filter(product=product, active=True)
    comments = product.comments.filter(active=True)
    total_comments_count = len(comments)

    # Pagination with 2 comments per page
    paginator = Paginator(comments, 3)
    page_number = request.GET.get("page", 1)
    try:
        comments = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer, deliver the first page
        comments = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range, deliver the last page of results
        comments = paginator.page(paginator.num_pages)

    return render(
        request,
        "shop/product/detail.html",
        {
            "product": product,
            "cart_product_form": cart_product_form,
            "recommended_products": recommended_products,
            "comment_form": comment_form,
            "comments": comments,
            "total_comments_count": total_comments_count,
        },
    )


def products_search(request):
    """
    The products_search function is a view that allows users to search for products.
    It uses the SearchForm form, which contains a single field named query. The user's input
    is stored in the query variable and then used to filter Product objects using Django's
    SearchVector and SearchQuery classes.

    :param request: Get the request object
    :return: A rendered template, but it also contains a form and query variables
    """
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
    try:
        r = Recommender()
        recommended_products = r.suggest_products_for([products], 4)
    except:
        recommended_products = []
    if len(recommended_products) == 0:
        all_products = Product.objects.filter(available=True)
        recommended_products = random.sample(list(all_products), min(len(all_products), 4))

    return render(
        request,
        "shop/product/search.html",
        {
            "form": form,
            "query": query,
            "results": results,
            "recommended_products": recommended_products,
        },
    )
