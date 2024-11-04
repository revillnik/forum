from typing import Any
from django import forms
from .models import Categories, Tags, Posts, Comments
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user

# @deconstructible
# class RussianValidator():
#     russian_dictionary = (
#         "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
#     )

#     def __call__(self, value, *args, **kwargs):
#         if not set(value) <= set(self.russian_dictionary):
#             raise ValidationError("Должен быть русский язык")


class Add_post_form(forms.ModelForm):
    title = forms.CharField(label="Заголовок",max_length=255, min_length=3,widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Заголовок"})),
    #      error_messages={
    #          "max_length": "Слишком длинный заголовок",
    #          "min_length": "Слишком короткий заголовок",
    #      },
    #  )
    #  slug = forms.SlugField(
    #      label="Slug",
    #      widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Slug"}),
    #      validators=[MaxLengthValidator(255, message="Слишком длинный Slug"), MinLengthValidator(3, message="Слишком короткий Slug")],
    #  )
    #  content = forms.CharField(
    #      label="Содержание",
    #      widget=forms.Textarea(
    #          attrs={"class": "form-control", "placeholder": "Содержание"}
    #      ),
    #  )
    #  title_photo = forms.ImageField(required=False, label="Изображение для главной страницы")
    #  tags = forms.ModelMultipleChoiceField(
    #      queryset=Tags.objects.all(),
    #      label="Теги",
    #  )
    cats = forms.ModelChoiceField(
         queryset=Categories.objects.all(),
         label="Категории", empty_label ="Нет категории",
         widget=forms.Select(attrs={"class": "form-control", "placeholder": "Категории"}),

     )
    #  def clean_title(self):
    #      russian_dictionary = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыьъэюя0123456789- "
    #      if not set(self.cleaned_data["title"]) <= set(russian_dictionary):
    #          raise ValidationError("Должен быть русский язык")
    #      else:
    #          return self.cleaned_data["title"]
    class Meta:
        model = Posts
        fields = ["title", "content", "title_photo", "tags", "cats"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Заголовок"},
            ),
            "content": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Содержание"},
            ),
            "cats": forms.Select(
                attrs={"class": "form-control", "placeholder": "Категории"},
            ),
        }
        labels = {
            "title": "Заголовок",
            "content": "Содержание",
            "title_photo": "Главное фото",
            "tags": "Теги",
            "cats": "Категории",
        }
    #   def clean_title(self):
    #       russian_dictionary = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    #       if not set(self.cleaned_data["title"]) <= set(russian_dictionary):
    #           raise ValidationError("Должен быть русский язык")
    #       else:
    #          return self.cleaned_data["title"]

class Edit_post_form(forms.ModelForm):
    cats = forms.ModelChoiceField(
        queryset=Categories.objects.all(),
        empty_label="Нет категории",
        label="Категории",
        widget=forms.Select(attrs={"class": "form-control", "placeholder": "Категории"})
    )
    def clean_title(self):
        russian_dictionary = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыьъэюя0123456789- "
        if not set(self.cleaned_data["title"]) <= set(russian_dictionary):
            raise ValidationError("Должен быть русский язык")
        else:
            return self.cleaned_data["title"]

    class Meta:
        model = Posts
        fields = ["title", "content", "title_photo", "tags", "cats"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Заголовок"},
            ),
            "content": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Содержание"},
            ),
            "cats": forms.Select(
                attrs={"class": "form-control", "placeholder": "Категории"},
            ),
        }
        labels = {
            "title": "Заголовок",
            "content": "Содержание",
            "title_photo": "Главное фото",
            "tags": "Теги",
            "cats": "Категории",
        }

class Add_comment_form(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(
                attrs={"class": "form-control", "cols": "30", "rows": "10"}
            ),
        }
        labels = {
            "message": "message",
        }
