# Generated by Django 4.2.1 on 2024-09-23 19:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0005_alter_posts_tags"),
    ]

    operations = [
        migrations.CreateModel(
            name="Categories",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cat_name", models.CharField(max_length=255, unique=True)),
                ("slug", models.SlugField(max_length=255, unique=True)),
            ],
        ),
    ]
