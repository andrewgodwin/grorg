from django.contrib import admin
from .models import Program

admin.site.register(
    Program,
    list_display = ["name", "completed"],
    prepopulated_fields = {"slug": ("name", )}
)
