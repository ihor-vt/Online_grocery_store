from django import forms
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _

from .models import ContactsUs, SubscribeEmailNewsletter


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "name": "name",
                "id": "name",
                "placeholder": _("Name"),
            }
        ),
        label="Full name",
        max_length=100,
    )
    email = forms.EmailField(
        label="Email",
        validators=[EmailValidator()],
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "name": "email",
                "id": "email",
                "placeholder": "Email",
            }
        ),
    )
    subject = forms.CharField(
        label="Subject",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "name": "subject",
                "id": "subject",
                "placeholder": _("Subject"),
            }
        ),
    )
    message = forms.CharField(
        label="Message",
        max_length=2000,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "name": "message",
                "id": "message",
                "placeholder": _("Message"),
            }
        ),
    )

    class Meta:
        model = ContactsUs
        fields = ["name", "email", "subject", "message"]


class SubscribeEmailNewsletterForm(forms.ModelForm):
    email = forms.EmailField(
        validators=[EmailValidator()],
        widget=forms.EmailInput(
            attrs={
                "class": "form-control border-0 shadow-0",
                "aria-describedby": "button-addon1",
                "name": "email",
                "type": "email",
                "placeholder": _("Enter your email address"),
            }
        ),
    )

    class Meta:
        model = SubscribeEmailNewsletter
        fields = ["email"]
