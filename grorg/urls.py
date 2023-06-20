from __future__ import annotations

from django.contrib import admin
from django.urls import include
from django.urls import path

from grants.views import bulk_load, program
from grorg.views import favicon
from users import views as users

urlpatterns = [
    path("favicon.ico", favicon),
    path("", program.index),
    path("accounts/", include("allauth.urls")),
    # path("login/", auth.views.LoginView.as_view(template_name="login.html")),
    # path("logout/", auth.views.LogoutView.as_view()),
    path("register/", users.register),
    path("join/", users.join),
    path("admin/", admin.site.urls),
    path("<str:program>/", program.ProgramHome.as_view()),
    path("<str:program>/questions/", program.ProgramQuestions.as_view()),
    path(
        "<str:program>/questions/<str:question_id>/",
        program.ProgramQuestionEdit.as_view(),
    ),
    path("<str:program>/apply/", program.ProgramApply.as_view()),
    path("<str:program>/apply/success/", program.ProgramApplySuccess.as_view()),
    path("<str:program>/applicants/", program.ProgramApplicants.as_view()),
    path("<str:program>/applicants/bulk/", bulk_load.BulkLoadApplicants.as_view()),
    path(
        "<str:program>/applicants/bulk_scores/",
        bulk_load.BulkLoadScores.as_view(),
    ),
    path("<str:program>/applicants/csv/", program.ProgramApplicantsCsv.as_view()),
    path(
        "<str:program>/applicants/random-unscored/",
        program.RandomUnscoredApplicant.as_view(),
    ),
    path(
        "<str:program>/applicants/<str:applicant_id>/",
        program.ProgramApplicantView.as_view(),
    ),
    path(
        "<str:program>/applicants/<str:applicant_id>/allocations/",
        program.ApplicantAllocations.as_view(),
    ),
    path("<str:program>/resources/", program.ProgramResources.as_view()),
    path(
        "<str:program>/resources/<str:resource_id>/",
        program.ProgramResourceEdit.as_view(),
    ),
]
