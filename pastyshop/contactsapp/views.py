from django.shortcuts import render, redirect
from django.contrib import messages as ms
from django.utils.translation import gettext_lazy as _

from .forms import ContactForm, SubscribeEmailNewsletterForm
from .tasks import contacts_us
from .messages_for_customers import thank_message, subscribe_message


def contacts(request):
    """
    The contacts function is a view that handles the contacts page.
    It renders the contact form and sends an email to the user with a thank you message.


    :param request: Get the request object
    :return: The contacts page with a form to send messages
    """
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
            return redirect("contacts:contacts")
    else:
        form = ContactForm()

    return render(
        request,
        "contactsapp/contacts.html",
        context={
            "form": form,
        },
    )


def subscribe_newsletter(request):
    """
    The subscribe_newsletter function is called when a user submits the newsletter subscription form.
    It takes in the request object, and if it's a POST request, it creates an instance of SubscribeEmailNewsletterForm with the data from that POST request.
    If that form is valid (i.e., all fields are filled out correctly), then we save its email field to our database and send an email to ourselves notifying us of this new subscriber.

    :param request: Get the data from the form
    :return: A redirect to the previous page
    """
    if request.method == "POST":
        form_newsletter = SubscribeEmailNewsletterForm(request.POST)
        if form_newsletter.is_valid():
            email = form_newsletter.cleaned_data["email"]
            form_newsletter.save()
            subject, message = subscribe_message(email)
            contacts_us.delay(email, subject, message)
    redirect_url = request.META.get("HTTP_REFERER", "/")
    return redirect(redirect_url)
