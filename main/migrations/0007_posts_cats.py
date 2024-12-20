# Generated by Django 4.2.1 on 2024-09-23 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0006_categories"),
    ]

    operations = [
        migrations.AddField(
            model_name="posts",
            name="cats",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="cats",
                to="main.categories",
            ),
        ),
    ]
