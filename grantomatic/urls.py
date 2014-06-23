from django.conf.urls import include, url
from django.contrib import admin
from grants import views

urlpatterns = [
    url(r'^$', 'grants.views.index'),
    url(r'^(?P<program>[^/]+)/$', views.ProgramHome.as_view()),
    url(r'^(?P<program>[^/]+)/questions/$', views.ProgramQuestions.as_view()),
    url(r'^(?P<program>[^/]+)/questions/(?P<question_id>[^/]+)/$', views.ProgramQuestionEdit.as_view()),
    url(r'^(?P<program>[^/]+)/apply/$', views.ProgramApply.as_view()),
    url(r'^(?P<program>[^/]+)/apply/success/$', views.ProgramApplySuccess.as_view()),
    url(r'^(?P<program>[^/]+)/applications/$', views.ProgramApplications.as_view()),
    url(r'^(?P<program>[^/]+)/applications/(?P<application_id>[^/]+)/$', views.ProgramApplicationView.as_view()),

    url(r'^admin/', include(admin.site.urls)),
]
