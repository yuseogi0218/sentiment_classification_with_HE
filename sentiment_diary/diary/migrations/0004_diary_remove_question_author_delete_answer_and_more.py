# Generated by Django 4.2.1 on 2023-05-17 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("diary", "0003_answer_author"),
    ]

    operations = [
        migrations.CreateModel(
            name="Diary",
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
                ("content", models.CharField(max_length=200)),
                ("sentiment", models.TextField()),
                ("create_date", models.DateTimeField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.RemoveField(model_name="question", name="author",),
        migrations.DeleteModel(name="Answer",),
        migrations.DeleteModel(name="Question",),
    ]
