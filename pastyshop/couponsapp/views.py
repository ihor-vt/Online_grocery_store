from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    """
    The coupon_apply function is a view that takes the coupon code from the form and
    checks if it exists in the database. If it does, then we store its ID in a session variable.
    If not, we set this session variable to None.

    :param request: Get the current session
    :return: A redirect to the cart_detail view
    """
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data["code"].strip()
        print(code, len(code), code.split())
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True,
            )
            request.session["coupon_id"] = coupon.id
        except Coupon.DoesNotExist:
            request.session["coupon_id"] = None
    return redirect("cart:cart_detail")
