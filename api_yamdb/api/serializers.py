from rest_framework import serializers

from django.contrib.auth import get_user_model

from reviews.models import Category, Comments, Genre, GenreTitle, Review, Title

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
        many=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        fields = '__all__'
        model = Title


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
        review = Review.objects.filter(
            title=self.context['title'],
            author=self.context['author']
        )
        if review.exists() and self.context['request.method'] == 'POST':
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
