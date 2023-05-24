from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Product


class ProductFilterForm(forms.Form):
    ORDER_CHOICES = [
        ("menu_order", _("Default sorting")),
        ("date", _("Sort by latest")),
        ("price", _("Sort by price: low to high")),
        ("price-desc", _("Sort by price: high to low")),
    ]

    orderby = forms.ChoiceField(
        choices=ORDER_CHOICES,
        label="Store Ordering",
        widget=forms.Select(attrs={"class": "orderby"}),
    )

    def apply_sorting(self, queryset):
        orderby = self.cleaned_data.get("orderby")

        if orderby == "price":
            queryset = queryset.order_by("price")
        elif orderby == "price-desc":
            queryset = queryset.order_by("-price")
        elif orderby == "date":
            queryset = queryset.order_by("-updated")

        return queryset


class SearchForm(forms.Form):
    query = forms.CharField()
