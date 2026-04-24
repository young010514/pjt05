from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("nickname", "interest_stocks", "profile_image")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("nickname", "interest_stocks", "profile_image")}),
    )
    list_display = ("username", "email", "nickname", "is_staff", "is_active")
    search_fields = ("username", "nickname", "email")

