from django.urls import path, include
from .views import PostsModelViewset, UserLists
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"posts", PostsModelViewset, basename="posts")
router.register(r"users", UserLists, basename="users")

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/drf-auth/", include("rest_framework.urls")),
]
