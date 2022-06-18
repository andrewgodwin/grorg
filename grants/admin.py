from __future__ import annotations

from django.contrib import admin

from .models import Answer, Applicant, Program, Score


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 1


admin.site.register(
    Program,
    list_display=["id", "name", "completed"],
    list_display_links=["id", "name"],
    prepopulated_fields={"slug": ("name",)},
)

admin.site.register(
    Applicant,
    list_display=["id", "name", "email", "program", "applied"],
    list_display_links=["id", "name"],
    inlines=[AnswerInline],
)

admin.site.register(
    Score,
    list_display=["id", "applicant", "user"],
)
