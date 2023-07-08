from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from user.models import User

from .validators import validate_year


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='строка идентификатор',
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='строка идентификатор',
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        ordering = ['name']


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произвидения',
        max_length=256,
    )
    year = models.IntegerField(
        verbose_name='Год создания',
        validators=[validate_year],
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='TitleGenre',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        ordering = ['name']


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


class CommonFieldsReviewCommentsAbstract(models.Model):
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(User,
                               verbose_name='автор', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        verbose_name='дата публикации', auto_now_add=True
    )

    class Meta:
        abstract = True


class Review(CommonFieldsReviewCommentsAbstract):
    title = models.ForeignKey(Title,
                              verbose_name='произведение',
                              on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(
        verbose_name='оценка',
        validators=[MinValueValidator(
            1, message='значение не должно быть меньше 1'),
            MaxValueValidator(
                10, message='значение не должно быть больше 10')])

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text


class Comment(CommonFieldsReviewCommentsAbstract):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               verbose_name='отзыв')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
