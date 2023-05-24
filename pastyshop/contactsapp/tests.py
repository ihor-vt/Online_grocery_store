from django.core import mail
from django.test import TestCase


class EmailTestCase(TestCase):
    def test_send_mail(self):
        mail.send_mail(
            'Example subject here',
            'Here is the message body.',
            'from@example.com',
            ['to@example.com'],
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Example subject here')
        self.assertEqual(mail.outbox[0].body, 'Here is the message body.')
        self.assertEqual(mail.outbox[0].from_email, 'from@example.com')
        self.assertEqual(mail.outbox[0].to, ['to@example.com'])
