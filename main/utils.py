from django.contrib import admin
from django.db.models import Count
import string


class Mixin_with_filter(admin.SimpleListFilter):
    title = "Наличие связанных постов"
    parameter_name = "status"
    name = None

    def lookups(self, request, model_admin):
        return [
            ("related", "Есть связанные посты"),
            ("no_related", "Нет связанных постов"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "related":
            return (
                queryset.all()
                .annotate(count_post=Count(self.name))
                .filter(count_post__gt=0)
            )
        elif self.value() == "no_related":
            return (
                queryset.all()
                .annotate(count_post=Count(self.name))
                .filter(count_post=0)
            )

class DataMixin:
    selected = None
    title = None
    extra_context = {}

    def __init__(self):
        if self.selected is not None:
            self.extra_context["selected"] = self.selected
        if self.title is not None:
            self.extra_context["title"] = self.title

    def get_context_data_mixin(self, context, **kwargs):
        context["selected"] = self.selected
        context["title"] = self.title
        context.update(kwargs)
        return context


def russian_in_english(text):
    dict = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "yo",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "c",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ь": "",
        "ы": "y",
        "ъ": "",
        "э": "r",
        "ю": "yu",
        "я": "ya",
        " ": "_",
    }
    s = ""
    for i in text.lower():
        s += dict[i]
    return s
