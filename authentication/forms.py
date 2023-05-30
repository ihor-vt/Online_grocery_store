from django import forms
from django.contrib.auth import password_validation
from django.core.validators import EmailValidator, RegexValidator
from django.utils.translation import gettext, gettext_lazy as _


phone_ua_validator = RegexValidator(
    regex=r"^\+38[0-9]{10}$",
    message='Введіть коректні дані без пробілів, дозволені символи: ", -"',
)

name_validator = RegexValidator(
    r"^[a-zA-Zа-яА-Яіїь'-]+$",
    message="Введіть коректні дані без пробілів, дозволені символи: ', -",
)

password_validator = RegexValidator(
    r"[A-Za-z0-9@#$%^&+=]{8,}",
    message="Пароль повинен містити мінімум 8 символів,\n1 велика літера, 1 маленька,1 цифра,один спец.символ",
)


class RegistrationForm(forms.Form):
    first_name = forms.CharField(
        label=_("First name"),
        validators=[name_validator],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "name": "first_name",
                "id": "first_name",
                "placeholder": "First name",
            }
        ),
    )
    last_name = forms.CharField(
        label=_("Last name"),
        validators=[name_validator],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "name": "last_name",
                "id": "last_name",
                "placeholder": "Last name",
            }
        ),
    )
    email = forms.EmailField(
        label=_("Email"),
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
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "type": "password",
                "name": "password",
                "id": "pswd",
                "placeholder": "Password",
            }
        ),
    )
    password2 = forms.CharField(
        label=_("Confirm password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "type": "password",
                "name": "password",
                "id": "pswd",
                "placeholder": "Confirm password",
            }
        ),
    )


class LoginForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
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
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "type": "password",
                "name": "password",
                "id": "pswd",
                "placeholder": "Password",
            }
        ),
    )


class EditUserInformationForm(forms.Form):
    first_name = forms.CharField(
        label="First name",
        validators=[name_validator],
        widget=forms.TextInput(attrs={"class": "search-input"}),
    )
    last_name = forms.CharField(
        label="Last name",
        validators=[name_validator],
        widget=forms.TextInput(attrs={"class": "search-input"}),
    )
    middle_name = forms.CharField(
        label="Middle name",
        validators=[name_validator],
        widget=forms.TextInput(attrs={"class": "search-input"}),
    )
    phone_number = forms.CharField(
        label="Phone number",
        validators=[phone_ua_validator],
        widget=forms.TextInput(attrs={"class": "search-input"}),
        help_text="Введіть номер телефону, формату +381234567891",
    )
    city = forms.CharField(
        label="City",
        widget=forms.TextInput(attrs={"class": "search-input"}),
        help_text="Введіть місто доставки",
    )
    street = forms.CharField(
        label="Street",
        widget=forms.TextInput(attrs={"class": "search-input"}),
        help_text="Введіть місто вулицю",
    )
    house_number = forms.CharField(
        label="House number",
        widget=forms.TextInput(attrs={"class": "search-input"}),
        help_text="Введіть номер будинку",
    )
    apartment_number = forms.CharField(
        label="Apartment number",
        widget=forms.TextInput(attrs={"class": "search-input"}),
        help_text="Введіть номер квартири",
    )


class AddUserInformationForm(forms.Form):
    first_name = forms.CharField(
        label="Ім'я",
        validators=[name_validator],
        widget=forms.TextInput(attrs={"class": "search-input"}),
    )
    last_name = forms.CharField(
        label="Прізвище",
        validators=[name_validator],
        widget=forms.TextInput(attrs={"class": "search-input"}),
    )
    middle_name = forms.CharField(
        label="По батькові",
        validators=[name_validator],
        widget=forms.TextInput(attrs={"class": "search-input"}),
    )
    email = forms.EmailField(
        label="Email",
        validators=[EmailValidator(message="Введіть коректний Email")],
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        help_text="Введіть Email, який буде використовуватися для входу на сайт.",
    )
    phone_number = forms.CharField(
        label="Мобільний телефон",
        validators=[phone_ua_validator],
        widget=forms.TextInput(attrs={"class": "search-input"}),
        help_text="Введіть номер телефону, формату +381234567891",
    )
    password1 = forms.CharField(
        label=_("Password"),
        validators=[password_validator],
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        validators=[password_validator],
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text=_("Enter the same password as before, for verification."),
    )
    city = forms.CharField(
        label="Місто",
        widget=forms.TextInput(attrs={"class": "search-input"}),
        help_text="Введіть місто доставки",
    )
    street = forms.CharField(
        label="Вулиця",
        widget=forms.TextInput(attrs={"class": "search-input"}),
        help_text="Введіть місто вулицю",
    )
    house_number = forms.CharField(
        label="Номер будинку",
        widget=forms.TextInput(attrs={"class": "search-input"}),
        help_text="Введіть номер будинку",
    )
    apartment_number = forms.CharField(
        label="Номер квартири",
        widget=forms.TextInput(attrs={"class": "search-input"}),
        help_text="Введіть номер квартири",
    )
