from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import CustomUser
from .forms import (
    RegistrationForm,
    LoginForm,
    EditUserInformationForm,
    AddUserInformationForm,
)


class UsersManagersTests(TestCase):
    def test_create_user(self):
        """
        The test_create_user function tests the creation of a user.
        It does so by creating a user with the create_user function, and then testing that:
            1) The email is correct.
            2) The active status is True (the default).
            3) The staff status is False (the default).  This means that this user cannot log into Django's admin site.  If you want to allow this, set it to True in your test case or use create_superuser instead of create_user.
            4) The superuser status is False (the default).  This means that this user cannot log into

        :param self: Represent the instance of the class
        :return: A user object
        """

        User = get_user_model()
        user = User.objects.create_user(
            first_name="Joe",
            last_name="Test_l",
            middle_name="Test_m",
            email="normal@user.com",
            password="foo",
        )
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(email="")

    def test_create_superuser(self):
        """
        The test_create_superuser function tests the creation of a superuser.
        It creates a user with all the attributes required for it to be considered
        a superuser, and then checks that those attributes are set correctly. It also
        tests that an error is raised if you try to create a non-superuser with
        is_superuser=False.

        :param self: Represent the instance of the class
        :return: A user that has the following properties:
        """

        User = get_user_model()
        admin_user = User.objects.create_superuser(
            first_name="Joe",
            last_name="Test_l",
            middle_name="Test_m",
            email="super@user.com",
            password="foo",
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )


class FormsTestCase(TestCase):
    def test_registration_form(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password1": "password123",
            "password2": "password123",
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form(self):
        form_data = {
            "email": "john.doe@example.com",
            "password": "password123",
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_edit_user_information_form(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "middle_name": "Middle",
            "phone_number": "+380674375471",
            "city": "City",
            "street": "Street",
            "house_number": "123",
            "apartment_number": "456",
        }
        form = EditUserInformationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_add_ivalid_user_information_form(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "+380674375471",
            "city": "City",
            "street": "Street",
            "house_number": "123",
            "apartment_number": "456",
            "password1": "password123",
            "password2": "password123",
        }
        form = AddUserInformationForm(data=form_data)
        self.assertFalse(form.is_valid())
