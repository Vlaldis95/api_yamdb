from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Comment, Review, User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'review', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Вы уже оставили отзыв')])

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'title', 'pub_date')
