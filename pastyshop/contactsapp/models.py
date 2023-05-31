from django.db import models


class ContactsUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=2000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.email}: {self.subject}"


class SubscribeEmailNewsletter(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return f"{self.email}"
