from django import forms
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _

from .models import Product, Comment


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


class CommentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", 
                                                        "name": "name",
                                                        "id": "name",
                                                        "placeholder": _("Name")}),
                                                        label="Full name",
                                                        max_length=100)
    email = forms.EmailField(label='Email', validators=[EmailValidator()],
                            widget=forms.EmailInput(attrs={"class": "form-control",
                                                            "name": "email",
                                                            "id": "email",
                                                            "placeholder":"Email"}))
    body = forms.CharField(label='Comment', max_length=150,
                            widget=forms.Textarea(attrs={"class": "form-control",
                                                        "name": "comment",
                                                        "id": "comment",
                                                        "placeholder": _("Comment")}))
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
