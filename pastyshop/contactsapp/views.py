from django.shortcuts import render, redirect
from django.contrib import messages as ms
from django.utils.translation import gettext_lazy as _

from .forms import ContactForm, SubscribeEmailNewsletterForm
from .tasks import contacts_us
from .messages_for_customers import thank_message, subscribe_message


def contacts(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            form.save()
            subject, messages = thank_message(name)
            # launch asynchronous task
            contacts_us.delay(email, subject, messages)
            ms.success(request, _("Your message has been received. Thank you!"))
            return redirect('contacts:contacts')
    else:
        form = ContactForm()

    return render(
        request, "contactsapp/contacts.html", context={"form": form,}
    )


def subscribe_newsletter(request):
    if request.method == 'POST':
        form_newsletter = SubscribeEmailNewsletterForm(request.POST)
        if form_newsletter.is_valid():
            email = form_newsletter.cleaned_data['email']
            form_newsletter.save()
            subject, message = subscribe_message(email)
            contacts_us.delay(email, subject, message)
    redirect_url = request.META.get('HTTP_REFERER', '/')
    return redirect(redirect_url)
