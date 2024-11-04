from rest_framework import serializers
from main.models import Posts, Tags
from django.contrib.auth import get_user_model


# class PostsSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     content = serializers.CharField()
#     slug = serializers.SlugField()
#     time_create = serializers.DateTimeField(read_only=True)

#     def create(self, validated_data):
#         return Posts.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.title = validated_data.get("title", instance.title)
#         instance.content = validated_data.get("content", instance.content)
#         instance.slug = validated_data.get("slug", instance.slug)
#         instance.time_create = validated_data.get("time_create", instance.time_create)
#         instance.save()
#         return instance


class PostsSerializer(serializers.ModelSerializer):
    cat_name = serializers.ReadOnlyField(source = "cats.cat_name", default = None)
    author_name = serializers.ReadOnlyField(source="author.username", default=None)
    tags_name = serializers.ReadOnlyField(source="tags.all.values", default=None)
    class Meta:
        model = Posts
        fields = [
            "id",
            "title",
            "content",
            "title_photo",
            "slug",
            "time_create",
            "tags_name",
            "tags",
            "cat_name",
            "cats",
            "author_name",
            "author",
        ]
        extra_kwargs = {
            "tags": {"write_only": True},
            "cats": {"write_only": True},
            "author": {"write_only": True},
        }

class UserListSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField("auth_posts")
    def auth_posts(self, obj):
        if Posts.objects.filter(author__id=obj.id):
           return list(Posts.objects.filter(author__id=obj.id).values('id', 'title'))
        else:
           return 'None'

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "first_name", "last_name", "posts"]
