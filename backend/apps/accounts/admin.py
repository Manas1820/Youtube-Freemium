from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from backend.apps.accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (_("Login info"), {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (_("Keyword"), {"fields": ("keyword",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "name"),
            },
        ),
    )
    list_filter = ("groups",)
    list_display = ("email", "name","keyword")
    search_fields = ("email", "name")
    ordering = ("email",)
