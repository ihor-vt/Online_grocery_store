from decimal import Decimal
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, reverse,\
                            get_object_or_404

from ordersapp.models import Order


# create the Stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def payment_process(request):
    """
    The payment_process function is the view that handles the payment process.
    It creates a Stripe checkout session and redirects to Stripe's payment form.
    
    :param request: Get the session data from stripe
    :return: A redirect to the stripe payment form
    """
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(
                            reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(
                            reverse('payment:canceled'))
        
        # Stripe checkout session data
        session_data = {
                'mode': 'payment',
                'client_reference_id': order.id,
                'success_url': success_url,
                'cancel_url': cancel_url,
                'line_items': []
        }
        
        # add order items to the Stripe checkout session
        for item in order.items.all():
            session_data['line_items'].append({
                    'price_data': {
                        'unit_amount': int(item.price * Decimal('100')),
                        'currency': 'usd',
                        'product_data': {
                            'name': item.product.name,
                        },
                    },
                    'quantity': item.quantity,
        })
            
        # Stripe coupon
        if order.coupon:
            stripe_coupon = stripe.Coupon.create(
                                name=order.coupon.code,
                                percent_off=order.discount,
                                duration='once')
            session_data['discounts'] = [{
                'coupon': stripe_coupon.id
            }]
            
        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        # redirect to Stripe payment form
        return redirect(session.url, code=303)
    else:
        return render(request, 'paymentapp/process.html', locals())
    

def payment_completed(request):
    """
    The payment_completed function is called by the Stripe API when a payment has been completed.
    It takes in a request object and returns an HTML page that displays to the user that their payment was successful.
    
    :param request: Get the request object
    :return: The completed
    """
    return render(request, 'paymentapp/completed.html')


def payment_canceled(request):
    """
    The payment_canceled function is called when the user cancels their payment.
    It renders a template that informs the user that they have canceled their payment.
    
    :param request: Get the request object
    :return: The canceled
    """
    return render(request, 'paymentapp/canceled.html')
