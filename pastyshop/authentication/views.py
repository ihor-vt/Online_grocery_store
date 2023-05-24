from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy
from django.contrib import messages

from django.contrib.auth import login as login_user, authenticate, logout
from django.contrib.auth.decorators import login_required

from .models import CustomUser
from .forms import (
    RegistrationForm,
    LoginForm,
    EditUserInformationForm,
    AddUserInformationForm,
)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "authentication/password_reset.html"
    email_template_name = "authentication/password_reset_email.html"
    html_email_template_name = "authentication/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")
    success_message = (
        "An email with instructions to reset your password has been sent to %(email)s."
    )
    subject_template_name = "authentication/password_reset_subject.txt"


def index(request):
    """
    The index function redirects the user to the registration page.

    :param request: Get the request from the user
    :return: A redirect to the registration page
    """
    return redirect("users:registration")


def registration(request):
    if request.method == "GET":
        form = RegistrationForm()
        return render(request, "authentication/register.html", {"form": form})
    
    elif request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            first_name = cd["first_name"]
            last_name = cd["last_name"]
            email = cd["email"]
            password = cd["password1"]
            password2 = cd["password2"]

            
            if password != password2:
                messages.warning(request, _("The passwords did not match"))
                return render(request, "authentication/register.html", {"form": form})
            
            if CustomUser.objects.filter(email=email).exists():
                messages.warning(request, _("Such an account is already registered"))
                return redirect("users:registration")
            
            hashed_password = make_password(password)

            user = CustomUser.create_user(
                email=email,
                password=hashed_password,
                first_name=first_name,
                last_name=last_name,
            )
            
            messages.success(request, _("You have successfully registered"))
            return redirect("users:login")
        
        else:
            return render(request, "authentication/register.html", {"form": form})
    
    return render(request, "authentication/register.html", {"form": form})


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "authentication/login.html", {"form": form})
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            if not email or not password:
                messages.warning(request, _("Fill in all fields"))
                return render(request, "authentication/login.html", {"form": form})

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login_user(request, user)
                return redirect("shop:product_list")
            else:
                messages.warning(request, _("Enter the correct data"))
                return render(request, "authentication/login.html", {"form": form})
        else:
            return render(request, "authentication/login.html", {"form": form})


@login_required
def specific_user(request, user_id):
    """
    The specific_user function takes in a request and an id,
        then it gets the user by that id.
        Then it creates a context with the user as its value.
        Finally, it renders the specificaluser template with that context.

    :param request: Get the request object, which is used to access the session
    :param id: Get the specific user by id
    :return: A specific user based on the id
    """
    if request.method == "GET":
        user = CustomUser.get_by_id(user_id)
        contex = {"user": user}
        return render(request, "authentication/specific_user.html", context=contex)
    elif request.method == "POST":
        return redirect("users:edit_user_information")


@login_required
def edit_user_information(request, user_id):
    """
    The edit_user_information function allows the user to edit their personal information.
        The function is called when a POST request is sent to the /edit_user_information/ URL.
        If the form data is valid, it saves changes in user's profile and redirects back to
        /edit_user_information/. Otherwise, it renders an empty form.

    :param request: Get the current request
    :return: A redirect to the edit_user_information page
    """
    user = CustomUser.get_by_id(user_id)
    if request.method == "POST":
        form = EditUserInformationForm(request.POST)
        if form.is_valid():
            # Збереження даних користувача
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.middle_name = form.cleaned_data["middle_name"]

            # Збереження адреси доставки
            user.phone_number = form.cleaned_data["phone_number"]
            user.city = form.cleaned_data["city"]
            user.street = form.cleaned_data["street"]
            user.house_number = form.cleaned_data["house_number"]
            user.apartment_number = form.cleaned_data["apartment_number"]
            user.save()
            contex = {"user": user}
            return render(request, "authentication/specific_user.html", context=contex)
    else:
        # Заповнення форми даними поточного користувача
        initial_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "middle_name": user.middle_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "city": user.city,
            "street": user.street,
            "house_number": user.house_number,
            "apartment_number": user.apartment_number,
        }

        form = EditUserInformationForm(initial=initial_data)

    context = {"form": form, "user": user}
    return render(request, "authentication/edit_user_information.html", context)


@login_required
def logoutuser(request):
    """
    The logoutuser function logs out the user and redirects them to the login page.


    :param request: Get the request object
    :return: The redirect function, which takes the user back to the login page
    """

    logout(request)
    return redirect("users:login")


def add_user_information(request):
    """
    The add_user_information function is used to add user information and if sucess auto regist and login user.
        Args:
            request (HttpRequest): The request object passed from the view.

    :param request: Get the request object
    :return: A render of the add_user_information

    """
    if request.method == "GET":
        form = AddUserInformationForm()
        return render(
            request, "authentication/add_user_information.html", {"form": form}
        )
    if request.method == "POST":
        form = AddUserInformationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            first_name = cd["first_name"]
            middle_name = cd["middle_name"]
            last_name = cd["last_name"]
            email = cd["email"]
            phone_number = cd["phone_number"]
            city = cd["city"]
            street = cd["street"]
            house_number = cd["house_number"]
            apartment_number = cd["apartment_number"]
            password1 = cd["password1"]
            password2 = cd["password2"]
            if password1 != password2:
                messages.add_message(request, messages.WARNING, "Паролі не зівпали")
            if messages.get_messages(request):
                return render(
                    request, "authentication/add_user_information.html", {"form": form}
                )
            else:
                CustomUser.create_user(
                    first_name,
                    middle_name,
                    last_name,
                    email,
                    phone_number,
                    password1,
                    city,
                    street,
                    house_number,
                    apartment_number,
                )
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Ви успішно ввели дані і зареєструвалися.",
                )
                user = CustomUser.objects.filter(email=email).first()
                if user:
                    session = authenticate(request, email=email, password=password1)
                    login_user(request, user)
                return redirect("shop:process")
        else:
            return render(
                request, "authentication/add_user_information.html", {"form": form}
            )
    else:
        return render(
            request, "authentication/add_user_information.html", {"form": form}
        )


def check_full_user_data(request):
    """
    The check_full_user_data function checks if the user is authenticated and has all of their information filled out.
    If they do, it redirects them to the specific_user page for that user. If not, it redirects them to add_user_information.

    :param request: Get the user object from the database
    :return: The user to the add_user_information page if their profile is incomplete
    """
    user = request.user
    if user.is_authenticated and user.check_all_user_data(user.email):
        contex = {"user": user}
        return render(request, "authentication/specific_user.html", context=contex)
    else:
        return redirect("users:add_user_information")
