from django.db import models

from .validators import validate_year


class Category(models.Model):
    name = models.CharField(
        verbose_name="Название категории",
        max_length=200
    )
    slug = models.SlugField(
        verbose_name="строка идентификатор",
        unique=True,
    )

    def __str__(self):
        return self.title


class Title(models.Model):
    name = models.CharField(
        verbose_name="Название произвидения",
        max_length=200,
    )
    year = models.IntegerField(
        verbose_name="Год создания",
        validators=[validate_year],
    )
    rating = models.IntegerField(
        verbose_name="Рейтинг",
        null=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True,
    )
    # genre = models.ForeignKey(
    #     Genre,
    #     related_name="titles",
    #     on_delete=models.SET_NULL
    #     null=True,
    # )
    category = models.ForeignKey(
        Category,
        related_name="titles",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Произведение"
