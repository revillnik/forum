from django import template
from main import views
from main.models import Posts, Tags, Categories
from django.core.cache import cache

register = template.Library()

@register.simple_tag()
def get_navigation():
    return views.navigation


@register.inclusion_tag("main/tags.html")
def get_all_tags(tag_selected):
    return {"all_tags": cache.get_or_set("all_tags", Tags.objects.all().prefetch_related("tags"), 60), "tag_selected": tag_selected}


@register.inclusion_tag("main/cats.html")
def get_all_cats(cat_selected):
    return {
        "all_cats": cache.get_or_set("all_cags", Categories.objects.all().prefetch_related("cats"), 60),
        "count_posts": cache.get_or_set("posts_counts", Posts.objects.all().count(), 60),
        "cat_selected": cat_selected,
    }
