import weasyprint

from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required

from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm
from .tasks import order_created


def order_create(request):
    """
    The order_create function is responsible for creating an order.
    It takes a request object as its only parameter and returns a rendered template.
    The function first creates an instance of the Cart class, passing it the current request object.
    If the HTTP method is POST, we create an instance of OrderCreateForm with the data from this POST request;
    if it's valid, we save it to our database (but not yet commit=True). We then check if there's any coupon in our cart;
    if so, we assign this coupon to our order and set its discount attribute accordingly. Then we save() again with commit=

    :param request: Get the cart from the session
    :return: An httpresponseredirect to the payment:process url
    """
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in the session
            request.session["order_id"] = order.id
            # redirect for payment
            return redirect(reverse("payment:process"))
    else:
        form = OrderCreateForm()
    return render(
        request, "ordersapp/order/create.html", {"cart": cart, "form": form}
    )


@staff_member_required
def admin_order_detail(request, order_id):
    """
    The admin_order_detail function is a view that renders the admin/ordersapp/order/detail.html template,
    which displays the details of an order in the Django admin interface.

    :param request: Pass the request object to the view
    :param order_id: Get the order object from the database
    :return: An html template
    """
    order = get_object_or_404(Order, id=order_id)
    return render(
        request, "admin/ordersapp/order/detail.html", {"order": order}
    )


@staff_member_required
def admin_order_pdf(request, order_id):
    """
    The admin_order_pdf function is a view that renders an HTML template to PDF.
    The function takes the order_id as a parameter and uses it to get the Order object from the database.
    Then, we use render_to_string() to render an HTML template with this Order object in context.
    Weasyprint converts this rendered HTML into PDF and returns it as HttpResponse.

    :param request: Get the order from the database
    :param order_id: Get the order object from the database
    :return: A pdf file
    """
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string("ordersapp/order/pdf.html", {"order": order})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename=order_{order.id}.pdf"
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / "css/pdf.css")],
    )
    return response
