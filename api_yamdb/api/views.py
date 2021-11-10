from rest_framework import filters, viewsets
from reviews.models import Category, Genre, Title
from api.serializers import CategorySerializer, GenreSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SignUpSerializer

User = get_user_model()

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer 
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category', 'genre', 'name', 'year')

class SignUpView(APIView):
    """Signup endpoint handler."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """Handle signup POST requests."""
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                settings.CONFIRMATION_EMAIL_HEADER,
                confirmation_code,
                settings.CONFIRMATION_EMAIL_SENDER,
                (user.email,)
            )

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
