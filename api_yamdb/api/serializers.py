import datetime as dt

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from django.contrib.auth import get_user_model

from reviews.models import Category, Comments, Genre, Review, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category requests."""

    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for genre requests."""
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleCreateSerializer(serializers.ModelSerializer):
    """Serializer for title requests."""
    rating = serializers.IntegerField()

    class Meta:
        fields = (
            'id',
            'name',
            'year', 
            'description', 
            'genre', 
            'category',
            'rating'
            )
        model = Title

    def validate_year(self, value):
        """Check the year."""
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Invalid value')
        return value


class SignUpSerializer(serializers.ModelSerializer):
    """Serializer for signup requests."""

    class Meta:
        model = User
        fields = ('email', 'username')
        unique = ('email', 'username')

    def validate_username(self, value):
        """Check if the username is not 'me'."""
        if value == 'me':
            raise serializers.ValidationError(
                'forbidden to use the name \'me\' as username.')
        return value

    def create(self, validated_data):
        """Create an user with validated data."""
        return User.objects.create_user(**validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for review requests."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    titles = serializers.SlugRelatedField(
        slug_field='name', queryset=Title.objects.all())

    def validate_score(self, score):
        """ Check that the score."""
        if score > 10 or score < 1:
            raise serializers.ValidationError("invalid value")
        return score

    class Meta:
        model = Review
        fields = '__all__'
        validators = (
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'titles')
            ),
        )


class CommentsSerializer(serializers.ModelSerializer):
    """Serializer for comments requests."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)

    class Meta:
        model = Comments
        fields = ('id', 'text', 'pub_date', 'author')


class TokenRequestSerializer(serializers.Serializer):
    """Serializer for token requests."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField

    class Meta:
        require_fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    """Custom User model serializer."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )

    def update(self, obj, validated_data):
        """Update user profile."""
        request = self.context.get('request')
        user = request.user

        is_admin = user.role == 'admin'
        if not user.is_superuser or not is_admin:
            validated_data.pop('role', None)

        return super().update(obj, validated_data)
