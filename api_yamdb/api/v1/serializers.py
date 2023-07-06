from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ParseError
from reviews.models import Category, Comment, Genre, Review, Title, User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        reviews = Review.objects.filter(title_id=obj.id)
        scores = [i.score for i in reviews]
        if len(scores) == 0:
            return 0
        return sum(scores) / len(scores)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id', )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    review = serializers.SlugRelatedField(slug_field='id', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'review', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='name', read_only=True)

    def validate(self, data):
        title_id = (
            self.context['request'].parser_context['kwargs']['title_id']
        )
        title = get_object_or_404(Title, pk=title_id)
        user = self.context['request'].user
        if (
            self.context['request'].method == 'POST'
            and Review.objects.filter(author=user, title=title).exists()
        ):
            raise ParseError(
                'Возможен только один отзыв на произведение!'
            )
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'title', "score", 'pub_date')
