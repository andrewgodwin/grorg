from django.contrib import admin
from .models import Program, Applicant, Score

admin.site.register(
    Program,
    list_display = ["id", "name", "completed"],
    list_display_links = ["id", "name"],
    prepopulated_fields = {"slug": ("name", )}
)

admin.site.register(
    Applicant,
    list_display = ["id", "name", "email", "program", "applied"],
    list_display_links = ["id", "name"],
)

admin.site.register(
    Score,
    list_display = ["id", "applicant", "user"],
)
