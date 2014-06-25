from django.conf.urls import include, url
from django.contrib import admin
from grants.views import program, bulk_load

urlpatterns = [
    url(r'^$', 'grants.views.program.index'),
    url(r'^login/$', 'users.views.login'),
    url(r'^logout/$', 'users.views.logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<program>[^/]+)/$', program.ProgramHome.as_view()),
    url(r'^(?P<program>[^/]+)/questions/$', program.ProgramQuestions.as_view()),
    url(r'^(?P<program>[^/]+)/questions/(?P<question_id>[^/]+)/$', program.ProgramQuestionEdit.as_view()),
    url(r'^(?P<program>[^/]+)/apply/$', program.ProgramApply.as_view()),
    url(r'^(?P<program>[^/]+)/apply/success/$', program.ProgramApplySuccess.as_view()),
    url(r'^(?P<program>[^/]+)/applicants/$', program.ProgramApplicants.as_view()),
    url(r'^(?P<program>[^/]+)/applicants/bulk/$', bulk_load.BulkLoadApplicants.as_view()),
    url(r'^(?P<program>[^/]+)/applicants/bulk_scores/$', bulk_load.BulkLoadScores.as_view()),
    url(r'^(?P<program>[^/]+)/applicants/random-unscored/$', program.RandomUnscoredApplicant.as_view()),
    url(r'^(?P<program>[^/]+)/applicants/(?P<applicant_id>[^/]+)/$', program.ProgramApplicantView.as_view()),
    url(r'^(?P<program>[^/]+)/applicants/(?P<applicant_id>[^/]+)/allocations/$', program.ApplicantAllocations.as_view()),
    url(r'^(?P<program>[^/]+)/resources/$', program.ProgramResources.as_view()),
    url(r'^(?P<program>[^/]+)/resources/(?P<resource_id>[^/]+)/$', program.ProgramResourceEdit.as_view()),

]
