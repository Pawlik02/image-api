from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Plan, User, Image, Height
from django.utils.translation import gettext as _


class PersonAdmin(UserAdmin):
    list_display = ['username', 'plan']
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_('Plan'), {'fields': ('plan',)}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
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
    )


admin.site.register(Plan)
admin.site.register(Image)
admin.site.register(Height)
admin.site.register(User, PersonAdmin)