from django.db import models
from django.urls import reverse
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.contrib.auth import get_user_model


class Posts(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
        validators=[MinLengthValidator(3)],
    )
    
    content = models.TextField(blank=True, verbose_name="Содержание")
    title_photo = models.ImageField(
        blank=True,
        null=True,
        default=None,
        upload_to="photos/%Y/%m/%d/",
        verbose_name="Главное фото",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
    )
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    tags = models.ManyToManyField(
        "Tags", blank=True, related_name="tags", verbose_name="Теги"
    )
    cats = models.ForeignKey(
        "Categories",
        blank=True,
        null=True,
        related_name="cats",
        on_delete=models.SET_NULL,
        verbose_name="Категории",
    )
    author = models.ForeignKey(get_user_model(), null = True, default = None, on_delete=models.SET_NULL, related_name="auth")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

class Tags(models.Model):
    tag_name = models.CharField(max_length=255, unique=True, verbose_name = "Назвение тега")
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.tag_name

    def get_absolute_url(self):
        return reverse("tag_posts", kwargs={"tag_slug": self.slug})

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Categories(models.Model):
    cat_name = models.CharField(max_length=255, unique=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.cat_name

    def get_absolute_url(self):
        return reverse("cat_posts", kwargs={"cat_slug": self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Comments(models.Model):
    author_name = models.CharField(max_length=255, verbose_name="Автор")
    email = models.EmailField()
    message = models.TextField(verbose_name = "Текст")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    post = models.ForeignKey(
        "Posts",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Пост",
    )

    def __str__(self):
        return f"{self.author_name}, {self.email}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
