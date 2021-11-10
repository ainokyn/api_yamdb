from rest_framework import serializers
from reviews.models import Category, Genre


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(slug_field='slug',read_only=True)

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        fields = '__all__'
        model = Genre
