from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Category, Product, Comment


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ["name", "slug"]
    # prepopulated_fields = {"slug": ("name",)}

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ["name", "slug", "price", "available", "created", "updated"]
    list_filter = ["available", "created", "updated"]
    list_editable = ["price", "available"]

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "product", "created", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["name", "email", "body"]
