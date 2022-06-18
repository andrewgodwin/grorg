from __future__ import annotations

from django.contrib import admin

from grants import models


class AnswerInline(admin.StackedInline):
    extra = 1
    model = models.Answer
    raw_id_fields = ["question"]
    readonly_fields = ["question", "answer"]


@admin.register(models.Allocation)
class AllocationAdmin(admin.ModelAdmin):
    raw_id_fields = ["applicant"]


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["applicant", "question"]
    raw_id_fields = ["applicant", "question"]
    readonly_fields = ["applicant", "question", "answer"]
    search_fields = ["applicant__name", "question__question"]


@admin.register(models.Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "program", "applied"]
    list_display_links = ["id", "name"]
    inlines = [AnswerInline]


@admin.register(models.Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "completed"]
    list_display_links = ["id", "name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        "program",
        "question",
        "order",
        "required",
        "type",
    ]
    list_filter = [
        "required",
        "type",
    ]
    raw_id_fields = ["program"]
    search_fields = ["question"]


@admin.register(models.Resource)
class ResourceAdmin(admin.ModelAdmin):
    raw_id_fields = ["program"]


@admin.register(models.Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ["id", "applicant", "user"]
    raw_id_fields = ["applicant", "user"]
    readonly_fields = ["applicant", "user", "score", "comment", "score_history"]


@admin.register(models.UploadedCSV)
class UploadedCSVAdmin(admin.ModelAdmin):
    pass
