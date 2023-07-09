from rest_framework import serializers
from reviews.models import Title, Review


class TitleAbstractSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        abstract = True
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def get_rating(self, obj):
        reviews = Review.objects.filter(title_id=obj.id)
        scores = [i.score for i in reviews]
        if len(scores) == 0:
            return None
        return sum(scores) / len(scores)
