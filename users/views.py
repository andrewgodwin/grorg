from django.contrib.auth import views as auth_views, authenticate, login as auth_login, re
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm, JoinForm
from .models import User

def login(request):
    return auth_views.login(request, template_name="login.html")

def logout(request):
    return auth_views.logout(request, next_page="/")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Make user
            user = User(
                email = form.cleaned_data['email'],
                name = form.cleaned_data['name'],
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Assign them to a program
            program = form.cleaned_data['program_code']
            program.users.add(user)
            program.save()
            # Log them in
            auth_login(
                request,
                authenticate(
                    email = form.cleaned_data['email'],
                    password = form.cleaned_data['password'],
                ),
            )
            return redirect("/")
    else:
        form = RegisterForm()
    return render(request, "register.html", {
        "form": form
    })

@login_required
def join(request):
    if request.method == "POST":
        form = JoinForm(request.POST)
        if form.is_valid():
            # Assign them to the program
            program = form.cleaned_data['program_code']
            program.users.add(request.user)
            program.save()
            return redirect("/")
    else:
        form = JoinForm()
    return render(request, "join.html", {
        "form": form
    })
