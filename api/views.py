from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from main.models import Posts, Comments
from rest_framework.response import Response
from django.forms.models import model_to_dict
from .serializers import PostsSerializer, UserListSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from .permissions import Reanonly_or_AllowAll, Reanonly_or_AllowAll_author
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

class ListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10000


class PostsModelViewset(viewsets.ModelViewSet):
    #  queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = (Reanonly_or_AllowAll_author,)
    pagination_class = ListPagination

    def get_queryset(self):
        if self.kwargs.get("pk"):
            return Posts.objects.filter(id=self.kwargs.get("pk"))
        return Posts.objects.all()

    @action(methods=['get'], detail=True)
    def post_comments(self, request, **kwargs):
        if Comments.objects.filter(post__id=kwargs.get("pk")):
            post_comments = Comments.objects.filter(post__id=kwargs.get("pk"))
            return Response({"comments": list(post_comments)})
        else:
            return Response({"comments": "Нет комментариев для данной статьи"})


class UserLists(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = get_user_model().objects.all()
    serializer_class = UserListSerializer

    @action(methods=['get'], detail=True)
    def auth_posts(self, request, **kwargs):
        if kwargs.get:
            posts_list = PostsSerializer(Posts.objects.filter(author__id=kwargs.get("pk")), many=True).data
            return Response({"Posts": posts_list})
        else: 
            return Response({"Posts": "У этого автора нет статей"})


# class ApiListPosts(generics.ListCreateAPIView):
#     queryset = Posts.objects.all()
#     serializer_class = PostsSerializer

# class DetailApiPosts(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Posts.objects.all()
#     serializer_class = PostsSerializer

# class ApiListPosts(APIView):

#     def get(self, request):
#         posts = Posts.objects.all().values()
#         return Response({"posts": list(posts)})

#     def post(self, request):
#         print(request.data)
#         post_new = Posts.objects.create(
#             title=request.data["title"],
#             content=request.data["content"],
#             slug=request.data["slug"],
#             title_photo=request.data["title_photo"],
#         )
#         return Response({"post": model_to_dict(post_new)})


# class ApiListPosts(APIView):

#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         try:
#             instance = Posts.objects.get(pk=pk)
#             instance.delete()
#             return Response({"delete_post": PostsSerializer(instance).data})
#         except:
#             raise Exception("pk did not find")

#     def get(self, request, *args, **kwargs):
#         posts = Posts.objects.all()
#         return Response({"posts": PostsSerializer(posts, many=True).data})

#     def post(self, request, *args, **kwargs):
#         serializer = PostsSerializer(data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"new_post": serializer.data})

#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         try:
#             instance = Posts.objects.get(pk=pk)
#         except:
#             raise Exception("pk did not find")
#         try:
#             serializer = PostsSerializer(data = request.data, instance=instance)
#             serializer.is_valid(raise_exception=True)
#             serializer = serializer.save()
#             return Response({"update_post": serializer.data})
#         except:
#             serializer = PostsSerializer(instance)
#             return Response({"post": serializer.data})
