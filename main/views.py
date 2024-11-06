from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from .models import Posts, Tags, Categories, Comments
from django.shortcuts import get_object_or_404
from .forms import Add_post_form, Edit_post_form, Add_comment_form
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from .utils import DataMixin, russian_in_english
from django.core.paginator import Paginator
from django import forms
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.core.mail import send_mail
from forum import settings
from django.core.cache import cache
from . import signals
from django.core.signals import request_finished
import string

# def index(request):
#     data = {"posts": Posts.objects.all().prefetch_related("tags", "comments").select_related("cats"), "selected": "index", "cat_selected": "all_cat"}
#     return render(request, "main/index.html", data)

# class index(TemplateView):
#     template_name = "main/index.html"
#     extra_context = {
#         "posts": Posts.objects.all().prefetch_related("tags", "comments").select_related("cats"),
#         "selected": "index",
#         "cat_selected": "all_cat",
#     }

# class index(ListView):
#     template_name = "main/index.html"
#     context_object_name = "posts"
#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context["selected"] = "index"
#         context["cat_selected"] = "all_cat"
#         return context
#     def get_queryset(self) -> QuerySet[Any]:
#         queryset = (
#             Posts.objects.all()
#             .prefetch_related("tags", "comments")
#             .select_related("cats")
#         )
#         return queryset


class index(DataMixin, ListView):
    template_name = "main/index.html"
    context_object_name = "posts"
    selected = "index"
    paginate_by = 10 # передает в шаблон page_obj - объект - текущую страницу, и paginator - объект пагинатор

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return self.get_context_data_mixin(
            context, cat_selected="all_cat", filter=self.request.GET.get("filter")
        )

    def get_queryset(self) -> QuerySet[Any]:
        if self.request.GET.get("filter"):
            queryset = (
                Posts.objects.filter(title__icontains=self.request.GET.get("filter"))
                .prefetch_related("tags", "comments")
                .select_related("cats")
            )
        else:
            queryset = cache.get_or_set(
                "all_posts",
                Posts.objects.all()
                .prefetch_related("tags", "comments")
                .select_related("cats"),
                60
            )
        return queryset


# class post(DetailView):
#     model = Posts
#     template_name = "main/post.html"
#     context_object_name = "post"
#     slug_url_kwarg = "post_slug"

#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context["selected"] = "post"
#         context["post_tags"] = context["post"].tags.all()
#         context["post_comments"] = Comments.objects.filter(post=context["post"])
#         return context


class post(DataMixin, DetailView):
    model = Posts
    template_name = "main/post.html"
    context_object_name = "post"
    slug_url_kwarg = "post_slug"
    selected = "post"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return self.get_context_data_mixin(
            context,
            post_tags=cache.get_or_set("all_tags_post", context["post"].tags.all(), 60),
            post_comments=Comments.objects.filter(post=context["post"])
        )     

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context["form"] = Add_comment_form()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = Add_comment_form(self.request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.author_name = self.request.user.username
            f.email = self.request.user.email
            f.post = self.object
            f.save()
            form = Add_comment_form()
        else: 
            form = Add_comment_form(self.request.POST)
        context["form"] = form
        return self.render_to_response(context)


#  def get_object(self, queryset = None) -> Model:
#     return get_object_or_404(Posts, slug = self.kwargs[self.slug_url_kwarg])


# def post(request, post_slug):
#     post = get_object_or_404(Posts, slug=post_slug)
#     data = {
#         "post_slug": post_slug,
#         "selected": "post",
#         "post": post,
#         "post_tags": post.tags.all(),
#         "post_comments": Comments.objects.filter(post=post),
#     }
#     return render(request, "main/post.html", data)


# def about(request):
#     data = {"selected": "about"}
#     return render(request, "main/about.html", data)

class about(DataMixin, TemplateView):
    template_name = "main/about.html"
    selected = "about"


def contact(request):
    if request.method == "POST":
        print(request.POST)
        send_mail(
            request.POST.get("name"),
            f'От организации: {request.POST.get("organization")} \n{request.POST.get("message")}',
            settings.EMAIL_HOST_USER,
            [request.POST.get("email")],
            fail_silently=False,
        )
        return redirect(request.META["HTTP_REFERER"], permanent=True)
    return render(request, "main/contact.html")


# def add_post(request):
#     if request.method == "POST":
#         form = Add_post_form(request.POST, request.FILES)
#         if form.is_valid():
#            form.save()
#            return redirect("index")

#     else:
#         form = Add_post_form()
#     data = {"selected": "add_post", "form": form}
#     return render(request, "main/add_post.html", data)

# class add_post(View):

#     def get(self, request):
#         form = Add_post_form()
#         data = {"selected": "add_post", "form": form}
#         return render(request, "main/add_post.html", data)

#     def post(self, request):
#         form = Add_post_form(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("index")
#         else:
#            data = {"selected": "add_post", "form": form}
#            return render(request, "main/add_post.html", data)

# class add_post(FormView):
#     form_class = Add_post_form
#     template_name = "main/add_post.html"
#     success_url = reverse_lazy("index")

#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context["selected"] = "add_post"
#         return context

#     def form_valid(self, form: Any) -> HttpResponse:
#         form.save()
#         print(self.request.POST["slug"])
#         return super().form_valid(form)

#     def get_success_url(self) -> str:
#         return reverse_lazy("post", kwargs={"post_slug": self.request.POST["slug"]})

# class add_post(CreateView):
#     form_class = Add_post_form
#     template_name = "main/add_post.html"
#     success_url = reverse_lazy("index")
#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context["selected"] = "add_post"
#         context["title"] = "Add post"
#         return context


# def add_comment(request, post_slug):
#     new_request_post = request.POST.copy()
#     new_request_post["post"] = Posts.objects.get(slug=post_slug)
#     form = Add_comment_form(new_request_post)
#     if form.is_valid():
#         form.save()
#         messages.success(request, "Комментарий добавлен!")
#     else:
#         messages.error(request,"Ошибка добавления комментария")

#     return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class add_post(LoginRequiredMixin, DataMixin, CreateView):
    form_class = Add_post_form
    template_name = "main/add_post.html"
    success_url = reverse_lazy("index")
    selected = "add_post"
    title = "Add post"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return self.get_context_data_mixin(context)

    def form_valid(self, form):
        f = form.save(commit=False) # используется чтобы через форму получить объект модели и в нем прописать значение поля "автор", 
        # ибо в самой форме нет такого поля, поэтому заходим через модель
        f.author = self.request.user
        if set(self.request.POST["title"].lower()).issubset(set(string.ascii_lowercase + ' ')):
            if not Posts.objects.filter(slug=slugify(str(self.request.POST["title"]))):
                f.slug = slugify(str(self.request.POST["title"]))
            else:
                form.add_error(
                    "title",
                    forms.ValidationError(
                        "Статья с таким slug и заголовком уже существует"
                    ),
                )
                return super().form_invalid(form)
        else:
            if not Posts.objects.filter(
                slug = russian_in_english(str(self.request.POST["title"]))
            ):
                f.slug = russian_in_english(str(self.request.POST["title"]))
            else:
                form.add_error(
                    "title",
                    forms.ValidationError(
                        "Статья с таким slug и заголовком уже существует"
                    ),
                )
                return super().form_invalid(form)
        return super().form_valid(form)


# class edit_post(UpdateView):
#     model = Posts
#     form_class = Edit_post_form
#     template_name = "main/add_post.html"
#     context_object_name = "form"
#     slug_url_kwarg = "post_slug"

#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context["selected"] = "edit_post"
#         context["title"] = "Edit post"
#         context["slug"] = self.kwargs["post_slug"]
#         return context

#     def get_success_url(self) -> str:
#         return reverse_lazy("post", kwargs={"post_slug": Posts.objects.get(title = self.request.POST["title"]).slug})


class edit_post(LoginRequiredMixin, DataMixin, UpdateView):
    model = Posts
    form_class = Edit_post_form
    template_name = "main/add_post.html"
    context_object_name = "form"
    slug_url_kwarg = "post_slug"
    selected = "edit_post"
    title = "Edit post"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return self.get_context_data_mixin(context, slug=self.kwargs["post_slug"])

    def get_success_url(self) -> str:
        return reverse_lazy(
            "post",
            kwargs={
                "post_slug": Posts.objects.get(title=self.request.POST["title"]).slug
            },
        )


class delete_post(LoginRequiredMixin, DeleteView):
    model = Posts
    slug_url_kwarg = "post_slug"

    def get_success_url(self):
        return self.request.META["HTTP_REFERER"]

# def tag_posts(request, tag_slug):
#     tag = get_object_or_404(Tags, slug=tag_slug)
#     posts = tag.tags.all()
#     data = {"posts": posts, "selected": "index", "tag_selected": tag}
#     return render(request, "main/index.html", data)

# class tag_posts(ListView):
#     template_name = "main/index.html"
#     context_object_name = "posts"
#     allow_empty = False

#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context["selected"] = "index"
#         context["tag_selected"] = get_object_or_404(Tags, slug=self.kwargs["tag_slug"])
#         return context

#     def get_queryset(self) -> QuerySet[Any]:
#         tag = get_object_or_404(Tags, slug=self.kwargs["tag_slug"])
#         queryset = tag.tags.all()
#         return queryset


class tag_posts(DataMixin, ListView):
    template_name = "main/index.html"
    context_object_name = "posts"
    allow_empty = False
    selected = "index"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return self.get_context_data_mixin(
            context, tag_selected=get_object_or_404(Tags, slug=self.kwargs["tag_slug"])
        )

    def get_queryset(self) -> QuerySet[Any]:
        tag = get_object_or_404(Tags, slug=self.kwargs["tag_slug"])
        queryset = cache.get_or_set(f"{tag.tag_name}_posts", tag.tags.all(), 60)
        return queryset


# class cat_posts(ListView):
#     template_name = "main/index.html"
#     context_object_name = "posts"
#     allow_empty = False

#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context["selected"] = "index"
#         context["cat_selected"] = get_object_or_404(Categories, slug = self.kwargs["cat_slug"])
#         return context
#     def get_queryset(self) -> QuerySet[Any]:
#         cat = get_object_or_404(Categories, slug=self.kwargs["cat_slug"])
#         queryset = cat.cats.all()
#         return queryset


class cat_posts(DataMixin, ListView):
    template_name = "main/index.html"
    context_object_name = "posts"
    allow_empty = False
    selected = "index"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return self.get_context_data_mixin(
            context,
            cat_selected=get_object_or_404(Categories, slug=self.kwargs["cat_slug"]),
        )

    def get_queryset(self) -> QuerySet[Any]:
        cat =  get_object_or_404(Categories, slug=self.kwargs["cat_slug"])
        queryset = cache.get_or_set(f"{cat.cat_name}_posts", cat.cats.all(), 60)
        return queryset


# def cat_posts(request, cat_slug):
#     cat = get_object_or_404(Categories, slug=cat_slug)
#     posts = Posts.objects.filter(cats = cat)
#     data = {"posts": posts, "selected": "index", "cat_selected": cat}
#     return render(request, "main/index.html", data)
