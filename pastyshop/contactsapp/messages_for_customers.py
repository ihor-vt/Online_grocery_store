from django.utils.translation import gettext_lazy as _

def thank_message(name):
    subject = _(f'Thank you for contacting the Pivfabrikati Team.')
    messages = _(f"""
    Dear {name},

    Thank you for reaching out to Pivfabrikati Store. We have received your inquiry and would like to express our sincere appreciation.

    Your message has been successfully received, and we are grateful for your interest. Our team has already begun reviewing your message
    and will make every effort to provide you with a comprehensive response as soon as possible. We value your time and will do our utmost 
    to ensure that you receive quality service and satisfaction with our semi-finished products.

    If you have any additional questions or need further assistance, please do not hesitate to contact us. We are always ready to provide 
    you with the support you need.

    Once again, thank you very much for contacting us. We appreciate your trust and value you as our customer.

    Best regards,
    Pivfabrikati Team
    """)

    return (subject, messages)


def subscribe_message(email):
    subject = _(f'Thank {email} for subscrib Pivfabrikati.')
    message = _("""
    Dear subscriber,

    Thank you for subscribing to the "Pivfabrykaty" store newsletter! We appreciate your 
    interest in our store and for choosing to receive our newsletter.

    You will be the first to receive updates on new products, special offers, 
    discounts, and much more. We strive to provide you with the best service and 
    unforgettable experiences with our products.

    If you have any questions, feel free to reach out to our customer support team. 
    We are always here to assist you.

    Thank you once again for your subscription. We are delighted to have you join our community!

    Best regards,
    The "Pivfabrykaty" Store Team
    """)

    return (subject, message)
