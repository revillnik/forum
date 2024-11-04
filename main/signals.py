from django.db.models.signals import pre_save, post_save, post_delete, m2m_changed
from django.core.signals import request_finished, request_started
from django.dispatch import receiver
from . models import Posts
from django.utils import timezone
from .views import index, post
# @receiver(pre_save, sender = Posts)
# def time_update(sender, instance, **kwargs):
#     instance.time_update = timezone.now()
#     print(timezone.now(), instance.time_update, instance)


# @receiver(post_save, sender = Posts)
# def created_message(sender, created, instance, **kwargs):
#     if created:
#         print(f"Был создан пост {instance.title}")
#     else:
#         print(f"Был изменен пост {instance.title}")

# @receiver(post_delete, sender = Posts)
# def deleted_message(sender, instance, **kwargs):
#     print(f"Был удален пост {instance.title}")

# @receiver(m2m_changed, sender = Posts.tags.through)
# def change_post_tags(sender, instance, model, pk_set, action, **kwargs):
#    print(f"Было совершено действие {action} над {model.objects.filter(id__in= pk_set)}")

# @receiver(request_finished)
# def index_finished(sender, **kwargs):
#     print("Функция представления завершилась")


# @receiver(request_started)
# def index_started(sender, environ, **kwargs):
#     print("Функция представления Началась", environ)
