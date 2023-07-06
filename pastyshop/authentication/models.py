from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser):
    """
    This class represents a basic user.
    Attributes:
    -----------
    param first_name: Describes first name of the user
    type first_name: str max length=20
    param last_name: Describes last name of the user
    type last_name: str max length=20
    param middle_name: Describes middle name of the user
    type middle_name: str max length=20
    param email: Describes the email of the user
    type email: str, unique, max length=100
    param password: Describes the password of the user
    type password: str
    param created_at: Describes the date when the user was created.
    Can't be changed.
    type created_at: int (timestamp)
    param updated_at: Describes the date when the user was modified
    type updated_at: int (timestamp)
    type updated_at: bool
    """

    first_name = models.CharField(max_length=20, default=None)
    last_name = models.CharField(max_length=20, default=None)
    middle_name = models.CharField(blank=True, max_length=20, null=True)
    phone_number = models.CharField(
        max_length=20, default=None, blank=True, null=True
    )
    email = models.EmailField(unique=True, max_length=100, default=None)
    password = models.CharField(max_length=255, default=None)
    city = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    house_number = models.CharField(max_length=10, blank=True, null=True)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    id = models.AutoField(primary_key=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    # def __str__(self) -> str:
    #     """
    #     Magic method is redefined to show all information about CustomUser.
    #     :return: user id, user first_name, user middle_name, user last_name,
    #             user email, user password, user updated_at, user created_at,
    #             user is_active
    #     """
    #     return (
    #         f"'first_name': '{self.first_name}', "
    #         f"'middle_name': '{self.middle_name}', "
    #         f"'last_name': '{self.last_name}', "
    #         f"'email': '{self.email}', "
    #         f"'created_at': {int(self.created_at.timestamp())\
    #                             if self.created_at else None}, "
    #         f"'updated_at': {int(self.updated_at.timestamp())\
    #                             if self.updated_at else None}, "
    #         f"'is_active': {self.is_active}"
    #     )

    def __repr__(self):
        """
        This magic method is redefined to show class and
        id of CustomUser object.
        :return: class, id
        """
        return f"{CustomUser.__name__}(id={self.id})"

    @staticmethod
    def get_by_id(user_id):
        """
        :param user_id: SERIAL: the id of a user to be found in the DB
        :return: user object or None if a user with such ID does not exist
        """
        custom_user = CustomUser.objects.filter(id=user_id).first()
        return custom_user if custom_user else None

    @staticmethod
    def get_by_email(email):
        """
        Returns user by email
        :param email: email by which we need to find the user
        :type email: str
        :return: user object or None if a user with such ID does not exist
        """
        custom_user = CustomUser.objects.filter(email=email).first()
        return custom_user if custom_user else None

    @staticmethod
    def delete_by_id(user_id):
        """
        :param user_id: an id of a user to be deleted
        :type user_id: int
        :return: True if object existed in the db and was removed
        or False if it didn't exist
        """
        user_to_delete = CustomUser.objects.filter(id=user_id).first()
        if user_to_delete:
            user_to_delete.delete()
            return True
        return False

    @staticmethod
    def create(
        email, password, first_name=None, middle_name=None, last_name=None
    ):
        """
        Creates a new user
        :param email: email of the user
        :type email: str
        :param password: password of the user
        :type password: str
        :param first_name: first name of the user
        :type first_name: str
        :param middle_name: middle name of the user
        :type middle_name: str
        :param last_name: last name of the user
        :type last_name: str
        :return: a new user object which is also written
        into the DB or None if user with this email
        is registered before.
        """
        if (
            email.split("@") == 2
            and len(CustomUser.objects.filter(email=email)) == 0
        ):
            custom_user = CustomUser(
                email=email,
                password=password,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
            )
            custom_user.save()
            return custom_user
        return None

    @staticmethod
    def create_user(
        first_name,
        last_name,
        email,
        password,
    ):
        """
        The create_user function creates a new user with the given
        email and password.
            Args:
                first_name (str): The first name of the user.
                last_name (str): The last name of the user.
                email (str): The email address for this user's account
                This will be used as their username when logging in
                to their account,
                so it must be unique across all users in our system!
                If an existing
                User already exists with this same email address,
                we'll return that
                User instead of creating a new one; otherwise we'll
                create a brand-new
                User object and save it to our database

        :param first_name: Set the first name of a user
        :param last_name: Create a last name for the user
        :param email: Check if the user already exists in the database
        :param password: Create a password for the user
        :param : Check if the user already exists in the database
        :return: The user object
        """

        user = CustomUser.get_by_email(email)
        if user:
            return user
        else:
            user = CustomUser(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            user.save()
            return user

    def to_dict(self):
        """
        The to_dict function is used to convert the User model
        into a dictionary.
        This function is called in the serializer, and it's
        purpose is to make sure
        that all of our data gets converted into JSON format.


        :param self: Represent the instance of the class
        :return: A dictionary with the information of a user
        """

        return {
            "id": self.id,
            "first_name": f"{self.first_name}",
            "middle_name": f"{self.middle_name}",
            "last_name": f"{self.last_name}",
            "email": f"{self.email}",
            "phone_number": f"{self.phone_number}",
            "city": f"{self.city}",
            "street": f"{self.street}",
            "house_number": f"{self.house_number}",
            "apartment_number": f"{self.apartment_number}",
            "created_at": int(self.created_at.timestamp()), 
            "updated_at": int(self.updated_at.timestamp()),
            "is_active": self.is_active,
        }

    @staticmethod
    def get_all():
        """
        The get_all function returns a list of all the users in the database.
            :return: A list of all users in the database.


        :return: All the users in the database
        """

        return CustomUser.objects.all()

    @staticmethod
    def check_all_user_data(email):
        """
        The check_all_user_data function checks if all the user
        data is filled in.


        :param email: Get the user object from the database
        :return: True if all the fields are not none
        """

        user = CustomUser.get_by_email(email)
        fields = [
            user.first_name,
            user.middle_name,
            user.last_name,
            user.email,
            user.password,
            user.phone_number,
            user.city,
            user.street,
            user.house_number,
            user.apartment_number,
        ]
        return all(field is not None for field in fields)

    def update(
        self,
        first_name=None,
        middle_name=None,
        last_name=None,
        email=None,
        password=None,
        is_active=None,
    ):
        """
        The update function takes in a user object and updates
        the fields of that user
        object with the values passed into it. If no value is
        passed for a field, then
        the field will not be updated. The function returns
        True if an update was made or False otherwise.

        :param self: Represent the instance of the object itself
        :param first_name: Update the first name of a user
        :param middle_name: Update the middle name of a user
        :param last_name: Set the last name of the user
        :param email: Find the user in the database
        :param password: Update the password of a user
        :param is_active: Determine if the user is active or not
        :param : Update the user's first name
        :return: True if the object existed in the db and
        was updated or false if it didn't exist
        """
        user_to_update = CustomUser.objects.filter(email=self.email).first()
        if first_name is not None and len(first_name) <= 20:
            user_to_update.first_name = first_name
        if middle_name is not None and len(middle_name) <= 20:
            user_to_update.middle_name = middle_name
        if last_name is not None and len(last_name) <= 20:
            user_to_update.last_name = last_name
        if len(email.split("@")) == 2:
            user_to_update.email = email
        if password is not None:
            user_to_update.password = password
        if is_active is not None:
            user_to_update.is_active = is_active
        user_to_update.save()

    def get_address(self):
        """
        The get_address function returns a string containing
        the user's address.
            The function will return the house number if it exists,
            or else it will
            return the apartment number.

        :param self: Refer to the current instance of a class
        :return: The address of the person
        """
        if self.house_number:
            h_namber = self.house_number
        elif self.apartment_number:
            h_namber = self.apartment_number

        return f"{self.city}, {self.street}, {h_namber}"

    def has_perm(self, perm, obj=None):
        """
        The has_perm function is used to determine if a user has the permission
        to perform an action. The function takes two arguments: perm and obj.
        The perm argument is a string representing the name of the permission,
        and obj represents an object on which this permission may be applied.
        If no object is passed in, then it will check for global permissions.

        :param self: Refer to the user object
        :param perm: Check if the user has a specific permission
        :param obj: Check if the user has permission
        to perform an action on a specific object
        :return: A boolean value
        """
        return self.is_superuser

    def has_module_perms(self, app_label):
        """
        The has_module_perms function is used to determine
        if the user has permissions to view any of the app’s models.
        This function returns True if the user is an active superuser.

        :param self: Represent the instance of the class
        :param app_label: Check if the user has permissions to view the app
        :return: True if the user is a superuser
        """
        return self.is_superuser
