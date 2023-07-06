from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    """
    The default UserAdmin class, but with changes for our CustomUser
    where `first_name` and `last_name` are replaced by `full_name` and
    `short_name`
    """

    fieldsets = (
        (None, {"fields": ("first_name", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "middle_name",
                    "last_name",
                    "email",
                    "phone_number",
                )
            },
        ),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser")},
        ),
        (
            _("Adress"),
            {"fields": ("city", "street", "house_number", "apartment_number")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {"classes": ("wide",), "fields": ("email", "password")},
        ),
    )

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.middle_name} {obj.last_name}"

    get_full_name.short_description = _("Full Name")

    list_display = ("email", "get_full_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "email")
    search_fields = ("email", "first_name", "middle_name", "last_name")
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
