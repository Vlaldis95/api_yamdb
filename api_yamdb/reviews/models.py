from django.contrib.auth.models import AbstractUser
from django.db import models
from .enums import UserRoles
from .validators import validate_username, validate_year

from .enums import UserRoles


class User(AbstractUser):
    """Класс пользователей."""

    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        db_index=True,
        validators=(validate_username,)
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='фамилия',
        blank=True
    )
    bio = models.TextField(
        verbose_name='биография',
        blank=True
    )
    role = models.CharField(
        max_length=20,
        verbose_name='роль',
        choices=UserRoles.choices(),
        default=UserRoles.user.name
    )
    need_send_code = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique'
            )
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == UserRoles.admin.name

    @property
    def is_moderator(self):
        return self.role == UserRoles.moderator.name

    @property
    def is_user(self):
        return self.role == UserRoles.user.name


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


class Review(models.Model):
    SCORE_CHOICES = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
                     (6, 6), (7, 7), (8, 8), (9, 9), (10, 10))
    title = models.ForeignKey(Title,
                              verbose_name='произведение',
                              on_delete=models.CASCADE)
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(User,
                               verbose_name='автор', on_delete=models.CASCADE)
    score = models.IntegerField(verbose_name='оценка',
                                choices=SCORE_CHOICES)
    pub_date = models.DateTimeField(
        verbose_name='дата публикации', auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(User,
                               verbose_name='автор', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        verbose_name='дата публикации', auto_now_add=True
    )
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               verbose_name='отзыв')

    def __str__(self):
        return self.text
