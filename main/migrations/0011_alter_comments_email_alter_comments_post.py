# Generated by Django 4.2.1 on 2024-10-11 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0010_alter_categories_options_alter_comments_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comments",
            name="email",
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name="comments",
            name="post",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="main.posts",
                verbose_name="Пост",
            ),
        ),
    ]
