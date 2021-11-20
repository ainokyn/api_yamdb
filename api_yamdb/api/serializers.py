from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comments, Genre, Review, Title

from .validate import validate_year

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


class TitleReadSerializer (serializers.ModelSerializer):
    """Title serializer for GET request."""
    rating = serializers.IntegerField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    """Title serializer for POST, PATCH request."""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        fields = '__all__'
        model = Title


class SignUpSerializer(serializers.ModelSerializer):
    """Serializer for signup requests."""
    username = serializers.CharField(
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )
    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )

    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate_username(self, value):
        """Check if the username is not 'me'."""
        if value == 'me':
            raise serializers.ValidationError(
                'forbidden to use the name \'me\' as username.')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for review requests."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField()

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ('id', 'pub_date', 'author', 'title')

    def validate_score(self, score):
        """ Check that the score."""
        if score > 10 or score < 1:
            raise serializers.ValidationError("invalid value")
        return score

    def validate(self, data):
        title_id = self.context.get(
            'request').parser_context['kwargs']['title_id']
        author = self.context.get('request').user
        review = Review.objects.filter(
            title_id=title_id,
            author=author
        )
        if review.exists() and self.context.get('request').method == 'POST':
            raise serializers.ValidationError(
                'Вы уже писали отзыв на это произведение.'
            )
        return data


class CommentsSerializer(serializers.ModelSerializer):
    """Serializer for comments requests."""
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comments


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
