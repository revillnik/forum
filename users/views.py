from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from .forms import UserRegistrationForm, login_form, UserProfileForm, UserPasswordChangeForm
from main.utils import DataMixin


class user_login(DataMixin, LoginView):
    form_class = login_form
    template_name = "users/login.html"
    selected = "login"
    title = "Login"
    success_url = reverse_lazy("index")


class user_register(DataMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")
    selected = "Registration"
    title = "Register"

#  def form_valid(self, form):
#     f = form.save(commit=False)
#     f.set_password(form.cleaned_data["password1"])
#     f.save()
#     return super().form_valid(form)


class user_profile(DataMixin, UpdateView):
    form_class = UserProfileForm
    template_name = "users/profile.html"
    pk_url_kwarg = "pk"
    selected = "Profile"
    title = "Profile"

    def get_object(self, queryset = ...):
        return self.request.user
    def get_success_url(self):
        return reverse("users:profile", args=[self.request.user.pk])


# def user_login(request):
#     if request.method == "POST":
#         form = login_form(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(
#                 request, username=cd["username"], password=cd["password"]
#             )
#             if user and user.is_active:
#                 login(request, user)
#                 return redirect("index")
#             else:
#                 return render(request, "users/login.html", {"form":form, "title": "login"})
#     else:
#         form = login_form()
#         return render(request, "users/login.html", {"form":form, "title": "login", "selected":"login"})


# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("users:login"))


class user_password_change(DataMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change.html"
    selected = "Profile"
    title = "Password change"

class user_password_change_done(DataMixin, PasswordChangeDoneView):
    template_name = "users/password_change_done.html"
    title = "Password change done"
