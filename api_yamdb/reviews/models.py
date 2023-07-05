from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


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
    title = models.TextField(verbose_name='заголовок')
    text = models.TextField(verbose_name='text')
    author = models.CharField(max_length=30, verbose_name='автор')
    score = models.IntegerField(verbose_name='оценка')
    pub_date = models.DateTimeField(
        verbose_name='дата публикации', auto_now_add=True
    )

    def __str__(self):
        return self.text
