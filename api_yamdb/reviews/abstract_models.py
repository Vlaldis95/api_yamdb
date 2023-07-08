from django.db import models


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
