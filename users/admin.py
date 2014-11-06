from django.contrib import admin
from .models import User


admin.site.register(
    User,
    list_display = ["id", "name", "email", "is_staff", "is_active"],
    list_display_links = ["id", "email"],
)
