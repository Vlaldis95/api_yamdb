from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username, validate_year

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    username = models.CharField(
        validators=(validate_username,),
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default='XXXX'
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username


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
        ordering = ['name']


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
        ordering = ['name']


class Title(models.Model):
    name = models.CharField(
        verbose_name="Название произвидения",
        max_length=256,
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


class Comment(models.Model):
    text = models.TextField(verbose_name='текст')
    author = models.CharField(max_length=30, verbose_name='автор')
    pub_date = models.DateTimeField(
        verbose_name='дата публикации', auto_now_add=True
    )
    review = models.ForeignKey('Review',
                               on_delete=models.CASCADE,
                               verbose_name='отзыв')

    def __str__(self):
        return self.text


class Review(models.Model):
    title = models.ForeignKey('Title',
                              verbose_name='произведение',
                              on_delete=models.CASCADE)
    text = models.TextField(verbose_name='текст')
    author = models.CharField(max_length=30, verbose_name='автор')
    score = models.IntegerField(verbose_name='оценка')
    pub_date = models.DateTimeField(
        verbose_name='дата публикации', auto_now_add=True
    )

    def __str__(self):
        return self.text
