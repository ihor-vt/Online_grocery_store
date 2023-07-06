import weasyprint
from io import BytesIO
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from ordersapp.models import Order
from pastyshop.settings import env


@shared_task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully paid.
    """
    order = Order.objects.get(id=order_id)
    # create invoice e-mail
    subject = f"My Shop - Invoice no. {order.id}"
    message = "Please, find attached the invoice for your recent purchase."
    email = EmailMessage(
        subject, message, env("EMAIL_HOST_USER"), [order.email]
    )
    # generate PDF
    html = render_to_string("ordersapp/order/pdf.html", {"order": order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / "css/pdf.css")]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # attach PDF file
    email.attach(f"order_{order.id}.pdf", out.getvalue(), "application/pdf")
    # send e-mail
    email.send()
