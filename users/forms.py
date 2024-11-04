from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.forms import ValidationError


class login_form(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    class Meta:
        model = get_user_model()
        fields = ["username", "password"]
        labels = {"username": "username", "password": "password"}
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control",}),
            "password": forms.PasswordInput(attrs={"class": "form-control",}),
        }


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Repeat password",
    )

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
        labels = {
            "username": "username",
            "email": "Email",
            "first_name": "First name",
            "last_name": "Last name",
            "password1": "Password",
            "password2": "Repeat password",
        }
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

   #  def clean_password1(self):
   #      if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
   #          return ValidationError("Пароли не совпадают")
   #      return self.cleaned_data["password1"]

    def clean_email(self):
        if get_user_model().objects.filter(email=self.cleaned_data["email"]).exists():
            return ValidationError("Пользователь с таким email уже существует")
        else:
            return self.cleaned_data["email"]

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(
        disabled=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.CharField(
        disabled=True, widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }
        labels = {
            "username": "username",
            "email": "Email",
            "first_name": "First name",
            "last_name": "Last name",
        }

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
