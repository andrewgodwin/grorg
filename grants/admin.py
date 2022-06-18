from __future__ import annotations

from django.contrib import admin

from grants import models


class AnswerInline(admin.StackedInline):
    model = models.Answer
    extra = 1


@admin.register(models.Allocation)
class AllocationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass


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
    pass


@admin.register(models.Resource)
class ResourceAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ["id", "applicant", "user"]


@admin.register(models.UploadedCSV)
class UploadedCSVAdmin(admin.ModelAdmin):
    pass
