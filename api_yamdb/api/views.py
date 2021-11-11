from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters, permissions, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import (CategorySerializer, CommentsSerializer,
                             GenreSerializer, ReviewSerializer)
from reviews.models import Category, Genre, Title

from .serializers import SignUpSerializer

User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    """Reviev endpoint handler."""
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """Overriding the get_queryset() method."""
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        reviews = title.reviews.all()
        return reviews

    def perform_create(self, serializer):
        """Overriding the perform_create() method."""
        title_id = self.kwargs['title_id']
        get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Overriding the perform_create() method."""
        title_id = self.kwargs['title_id']
        get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):
    """Comments endpoint handler."""
    serializer_class = CommentsSerializer

    def get_queryset(self):
        """Overriding the get_queryset() method."""
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        title = get_object_or_404(Title, id=title_id)
        review = get_object_or_404(title.reviews.all, id=review_id)
        comments = review.comments.all()
        return comments

    def perform_create(self, serializer):
        """Overriding the perform_create() method."""
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        title = get_object_or_404(Title, id=title_id)
        get_object_or_404(title.reviews.all, id=review_id)
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Overriding the perform_update() method."""
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        title = get_object_or_404(Title, id=title_id)
        get_object_or_404(title.reviews.all, id=review_id)
        serializer.save(author=self.request.user)


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
