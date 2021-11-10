from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


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
