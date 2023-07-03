from django.db import models


class Comment(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=30)
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    review = models.ForeignKey('Review', on_delete=models.CASCADE)


class Review(models.Model):
    title = models.TextField()
    text = models.TextField()
    author = models.CharField(max_length=30)
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )


class Title(models.Model):
    text = models.TextField()
