from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from .models import Posts, Tags, Categories, Comments
from django.db.models import Count
from django.utils.safestring import mark_safe
from .utils import Mixin_with_filter


class With_tags(Mixin_with_filter, admin.SimpleListFilter):
    name = "tags"


class With_cats(Mixin_with_filter, admin.SimpleListFilter):
    name = "cats"


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    filter_horizontal = ["tags"]
    prepopulated_fields = {"slug": ("title", )}
    list_display = (
        "pk",
        "slug",
        "title",
        "main_photo",
        "time_create",
        "cats",
        "related_tags",
        "author",
    )
    fields = (
        "slug",
        "title",
        "content",
        "title_photo",
        "main_photo",
        "time_create",
        "cats",
        "related_tags",
        "author",
    )
    readonly_fields = (
        "time_create",
        "related_tags",
        "main_photo",
    )
    list_display_links = (
        "pk",
        "slug",
    )
    ordering = ("-time_create", "pk",)
    list_editable = (
        "cats",
        "title"
    )
    list_select_related = True
    list_per_page = 10
    actions = [
        "delete_tags",
    ]
    search_fields = (
        "title__icontains",
        "slug__icontains",
        "cats__cat_name__icontains",
        "tags__tag_name__icontains",
    )
    list_filter = ["cats", "tags",]

    @admin.display(description="Связанные теги")
    def related_tags(self, Posts):
        tags = Posts.tags.all()
        list_tags = list()
        for i in tags:
            list_tags.append(i.tag_name)
        if tags:
            return f"{", ".join(list_tags)}"
        else: 
            return "Нет"

    @admin.display(description="Главная фотография")
    def main_photo(self, Posts):
        if Posts.title_photo:
            return mark_safe(f"<img src='{Posts.title_photo.url}' width=50>")
        else:
            return ("Нет фото")

    @admin.action(description="Убрать все теги")
    def delete_tags(self, request, queryset):
        for i in queryset:
            i.tags.clear()
        count = queryset.count()
        self.message_user(request, f"У {count} статей были убраны теги!", messages.WARNING)


@admin.register(Tags)
class PostsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("tag_name",)}
    list_display = ("pk", "slug", "tag_name", "related_posts")
    list_display_links = ("pk", "slug")
    ordering = ("tag_name",)
    list_editable = ("tag_name",)
    list_select_related = True
    list_per_page = 10
    actions = ["delete_posts",]
    search_fields = (
        "tag_name__icontains",
        "tags__title__icontains",
    )
    list_filter = (With_tags, "tags",)

    @admin.display(description="Связанные статьи")
    def related_posts(self, Tags):
        posts = Tags.tags.all()
        list_posts = list()
        for i in posts:
            list_posts.append(i.title)
        if posts:
            return f"{", ".join(list_posts)}"
        else:
            return "Нет"

    @admin.action(description="Убрать все посты")
    def delete_posts(self, request, queryset):
        for i in queryset:
            i.tags.clear()
        count = queryset.count()
        self.message_user(
            request, f"У {count} тегов были убраны статьи!", messages.WARNING)


@admin.register(Categories)
class PostsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("cat_name",)}
    list_display = (
        "pk",
        "slug",
        "cat_name",
        "related_posts",
    )
    list_display_links = ("pk", "slug")
    ordering = ("cat_name",)
    list_editable = ("cat_name",)
    list_select_related = True
    list_per_page = 10
    actions = [
        "delete_posts",
    ]
    search_fields = (
        "cat_name__icontains",
        "cats__title__icontains",
    )
    list_filter = [With_cats,]

    @admin.display(description="Связанные статьи")
    def related_posts(self, Categories):
        posts = Categories.cats.all()
        list_posts = list()
        for i in posts:
            list_posts.append(i.title)
        if posts:
            return f"{", ".join(list_posts)}"
        else:
            return "Нет"

    @admin.action(description="Убрать все посты")
    def delete_posts(self, request, queryset):
        for i in queryset:
            i.cats.clear()
        count = queryset.count()
        self.message_user(
            request, f"У {count} категорий были убраны статьи!", messages.WARNING
        )

@admin.register(Comments)
class PostsAdmin(admin.ModelAdmin):
    list_display = ("pk", "author_name", "email", "time_create", "post")
    list_display_links = ("pk", "author_name")
    ordering = ("-time_create",)
    list_select_related = True
    list_per_page = 10
    search_fields = (
        "author_name__icontains",
        "email__icontains",
        "post__title__icontains",
    )
    list_filter = ("author_name",)
