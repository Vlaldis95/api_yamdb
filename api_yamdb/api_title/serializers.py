from rest_framework import serializers

from .models import Title, Category


class TitleSerializer(serializers.ModelSerializer):
    # genre = serializers.PrimaryKeyRelatedField(
    #     queryset=Genre.objects.all()
    # )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )

    class Meta:
        model = Title
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
