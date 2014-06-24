from django.contrib import admin
from .models import Program, Applicant

admin.site.register(
    Program,
    list_display = ["name", "completed"],
    prepopulated_fields = {"slug": ("name", )}
)

admin.site.register(
    Applicant,
    list_display = ["name", "email", "program", "applied"],
)
