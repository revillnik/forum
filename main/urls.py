from django.urls import path
from main import views
from django.core.cache import cache
from django.views.decorators.cache import cache_page


urlpatterns = [
    path("", views.index.as_view(), name="index"),
    path("post/<slug:post_slug>/", views.post.as_view(), name="post"),
    #  path(
    #      "add_comment/<slug:post_slug>/", views.add_comment, name="add_comment"
    #  ),
    path("about/", cache_page(60)(views.about.as_view()), name="about"),
    path("contact/", views.contact, name="contact"),
    path("add_post/", views.add_post.as_view(), name="add_post"),
    path("tag/<slug:tag_slug>/", views.tag_posts.as_view(), name="tag_posts"),
    path("cat/<slug:cat_slug>/", views.cat_posts.as_view(), name="cat_posts"),
    path("edit/<slug:post_slug>/", views.edit_post.as_view(), name="edit_post"),
    path("delete/<slug:post_slug>/", views.delete_post.as_view(), name="delete_post"),
]
