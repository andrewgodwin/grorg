from django.conf.urls import include, url
from django.contrib import admin
from grants import views

urlpatterns = [
    url(r'^$', 'grants.views.index', name='index'),
    url(r'^(?P<program>[^/]+)/$', views.ProgramHome.as_view(), name='program-home'),
    url(r'^(?P<program>[^/]+)/questions/$', views.ProgramQuestions.as_view(), name='program-questions'),
    url(r'^(?P<program>[^/]+)/questions/(?P<question_id>[^/]+)/$', views.ProgramQuestionEdit.as_view(), name='program-question-edit'),

    url(r'^admin/', include(admin.site.urls)),
]
