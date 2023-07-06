from .forms import SubscribeEmailNewsletterForm


def newsletter_form(request):
    form_newsletter = SubscribeEmailNewsletterForm()
    return {"form_newsletter": form_newsletter}
