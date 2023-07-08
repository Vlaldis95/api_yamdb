from django.db import models

from user.models import User


class SlugAndNameAbstractModel(models.Model):

    class Meta:
        abstract = True

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


class CommonFieldsReviewCommentsAbstract(models.Model):
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(User,
                               verbose_name='автор', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        verbose_name='дата публикации', auto_now_add=True
    )

    class Meta:
        abstract = True