from django.db import models

from .validators import validate_year


class Genre(models.Model):
    name = models.CharField(
        verbose_name="Название жанра",
        max_length=200
    )
    slug = models.SlugField(
        verbose_name="строка идентификатор",
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"


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
        return self.name

    class Meta:
        verbose_name = "Категория"


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
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Жанр",
        through='TitleGenre',
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        related_name="titles",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Произведение"


class TitleGenre(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        null=True)

    def __str__(self):
        return f'{self.title} - {self.genre}'
