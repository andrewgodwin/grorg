from django.contrib.auth import views as auth_views

def login(request):
    return auth_views.login(request, template_name="login.html")

def logout(request):
    return auth_views.logout(request, next_page="/")
