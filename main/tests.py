from django.test import TestCase
from django.urls import reverse, reverse_lazy
from .models import Posts, Categories, Tags, Comments
from http import HTTPStatus
from django.contrib.auth.models import User
from django.core.cache import cache


class AboutTestCase(TestCase):

    def setUp(self):
        cache.clear()

    def test_view(self):
        path = reverse("about")
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["selected"], "about")
        self.assertTemplateUsed(response, "main/about.html")


class CatTagFilterTestCase(TestCase):
    fixtures = [
        "cats.json",
        "posts.json",
        "tags.json",
    ]

    def setUp(self):
        cache.clear()
        self.posts = Posts.objects.all()
        self.category = Categories.objects.first()
        self.tag = Tags.objects.first()

    def __test_common(
        self, response
    ):  # здесь делаем закрытую функцию, чтобы она не вопсринималась как тест
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["selected"], "index")
        self.assertTemplateUsed(response, "main/index.html")

    def test_cat(self):
        path = reverse("cat_posts", kwargs={"cat_slug": self.category.slug})
        response = self.client.get(path)

        self.__test_common(response)

        self.assertEqual(response.context["cat_selected"], self.category)
        self.assertEqual(
            list(response.context["posts"]),
            list(self.posts.filter(cats__slug=self.category.slug)),
        )

    def test_tag(self):
        path = reverse("tag_posts", kwargs={"tag_slug": self.tag.slug})
        response = self.client.get(path)

        self.__test_common(response)

        self.assertEqual(response.context["tag_selected"], self.tag)
        self.assertEqual(
            list(response.context["posts"]),
            list(self.posts.filter(tags__slug=self.tag.slug)),
        )

    def test_filter(self):
        path = reverse("index")
        response_filter = self.client.get(path, {"filter": "о"})
        self.__test_common(response_filter)
        list_all_objects = list()
        for i in response_filter.context["paginator"].page_range:
            list_all_objects += list(
                response_filter.context["paginator"].page(i).object_list
            )
        self.assertEqual(
            list_all_objects,
            list(
                self.posts.filter(
                    title__icontains=str(response_filter.context["filter"])
                )
            ),
        )
        response_without_filter = self.client.get(path)
        list_all_objects.clear()
        for i in response_without_filter.context["paginator"].page_range:
            list_all_objects += list(
                response_without_filter.context["paginator"].page(i).object_list
            )
        self.assertEqual(
            list_all_objects,
            list(self.posts.all()),
        )


class PostTestCase(TestCase):
    fixtures = ["cats.json", "posts.json", "tags.json", "users.json"]

    def setUp(self):
        cache.clear()
        self.post = Posts.objects.first()

    def __test_common(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "main/post.html")
        self.assertEqual(response.context["selected"], "post")
        self.assertEqual(response.context["post"], self.post)
        self.assertEqual(
            list(response.context["post_tags"]), list(self.post.tags.all())
        )
        self.assertEqual(
            list(response.context["post_comments"]), list(self.post.comments.all())
        )

    def test_post_get(self):
        path = reverse("post", kwargs={"post_slug": self.post.slug})
        response = self.client.get(path)

        self.__test_common(response)

    def test_post_post(self):
        path = reverse("post", kwargs={"post_slug": self.post.slug})
        data = {
            "author_name": "root",
            "email": "revillnik@mail.ru",
            "message": "root",
            "post": 23,
        }

        self.assertFalse(Comments.objects.filter(email="revillnik@mail.ru").exists())

        self.client.login(username="root", password="2215779638d")
        response = self.client.post(path, data)

        self.__test_common(response)

        self.assertTrue(Comments.objects.filter(email="revillnik@mail.ru").exists())


class AddPostTestCase(TestCase):
    fixtures = ["cats.json", "posts.json", "tags.json", "users.json"]

    def setUp(self):
        cache.clear()
        self.post = Posts.objects.first()
        self.path = reverse("add_post")

    def test_get(self):
        self.client.login(username="root", password="2215779638d")
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "main/add_post.html")
        self.assertEqual(response.context["selected"], "add_post")
        self.assertEqual(response.context["title"], "Add post")

    def test_post(self):
        self.client.login(username="root", password="2215779638d")
        data = {
            "title": "asdasd",
            "content": "Содержание",
            "title_photo": "None",
            "tags": Tags.objects.first().id,
            "cats": Categories.objects.first().id,
        }

        self.assertFalse(Posts.objects.filter(title="asdasd").exists())

        response = self.client.post(self.path, data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("index"))
        self.assertTrue(Posts.objects.filter(title="asdasd").exists())

        Posts.objects.filter(title="asdasd").delete()



class EditDeletePostTestCase(TestCase):
    fixtures = ["cats.json", "posts.json", "tags.json", "users.json"]

    def setUp(self):
        cache.clear()
        self.post = Posts.objects.first()
        self.path = reverse("edit_post", kwargs={"post_slug": self.post.slug})

    def test_get(self):
        self.client.login(username="root", password="2215779638d")

        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "main/add_post.html")
        self.assertEqual(response.context["selected"], "edit_post")
        self.assertEqual(response.context["title"], "Edit post")
        self.assertEqual(response.context["object"], self.post)

    def test_post(self):
        self.client.login(username="root", password="2215779638d")
        data = {
            "title": "тест статья",
            "content": "Содержание",
            "title_photo": "None",
            "tags": Tags.objects.first().id,
            "cats": Categories.objects.first().id,
        }

        response = self.client.post(self.path, data, follow=True)

        self.assertEqual(data["title"], Posts.objects.get(title=data["title"]).title)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(
            response,
            reverse("post", kwargs={"post_slug": response.context["object"].slug}),
        )
    def test_delete_post(self):
        self.client.login(username="root", password="2215779638d")
        path = reverse_lazy("delete_post", kwargs={"post_slug": Posts.objects.first().slug})

        delete_post = Posts.objects.first()

        response = self.client.post(path, follow=True, HTTP_REFERER=reverse("index"))

        self.assertNotEqual(Posts.objects.first(), delete_post)
