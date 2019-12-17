from django.contrib import admin, auth
from django.urls import path, re_path
from grants.views import program, bulk_load
from users import views as users

urlpatterns = [
    path('', program.index),
    path("login/", auth.views.LoginView.as_view(template_name="login.html")),
    path("logout/", auth.views.LogoutView.as_view()),
    path('register/', users.register),
    path('join/', users.join),
    path('admin/', admin.site.urls),
    re_path(r'^(?P<program>[^/]+)/$', program.ProgramHome.as_view()),
    re_path(r'^(?P<program>[^/]+)/questions/$', program.ProgramQuestions.as_view()),
    re_path(r'^(?P<program>[^/]+)/questions/(?P<question_id>[^/]+)/$', program.ProgramQuestionEdit.as_view()),
    re_path(r'^(?P<program>[^/]+)/apply/$', program.ProgramApply.as_view()),
    re_path(r'^(?P<program>[^/]+)/apply/success/$', program.ProgramApplySuccess.as_view()),
    re_path(r'^(?P<program>[^/]+)/applicants/$', program.ProgramApplicants.as_view()),
    re_path(r'^(?P<program>[^/]+)/applicants/bulk/$', bulk_load.BulkLoadApplicants.as_view()),
    re_path(r'^(?P<program>[^/]+)/applicants/bulk_scores/$', bulk_load.BulkLoadScores.as_view()),
    re_path(r'^(?P<program>[^/]+)/applicants/random-unscored/$', program.RandomUnscoredApplicant.as_view()),
    re_path(r'^(?P<program>[^/]+)/applicants/(?P<applicant_id>[^/]+)/$', program.ProgramApplicantView.as_view()),
    re_path(r'^(?P<program>[^/]+)/applicants/(?P<applicant_id>[^/]+)/allocations/$', program.ApplicantAllocations.as_view()),
    re_path(r'^(?P<program>[^/]+)/resources/$', program.ProgramResources.as_view()),
    re_path(r'^(?P<program>[^/]+)/resources/(?P<resource_id>[^/]+)/$', program.ProgramResourceEdit.as_view()),

]
