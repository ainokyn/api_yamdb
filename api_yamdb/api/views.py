from django.http import request
from rest_framework import filters, pagination, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.db.models.aggregates import Avg

from reviews.models import Category, Genre, Review, Title

from .permissions import AnonymModeratorAdminAuthor, IsAdmin, IsAdminOrReadOnly
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerializer,
                          TitleSerializer, TokenRequestSerializer,
                          UserSerializer)

User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    """Review endpoint handler."""
    serializer_class = ReviewSerializer
    permission_classes = (AnonymModeratorAdminAuthor,)

    def get_queryset(self):
        """Overriding the get_queryset() method."""
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

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
    permission_classes = (AnonymModeratorAdminAuthor,)
    serializer_class = CommentsSerializer

    def get_queryset(self):
        """Overriding the get_queryset() method."""
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        title = get_object_or_404(Title, id=title_id)
        reviews = get_object_or_404(title.reviews, id=review_id)
        return reviews.comments.all()

    def perform_create(self, serializer):
        """Overriding the perform_create() method."""
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        title = get_object_or_404(Title, id=title_id)
        get_object_or_404(title.reviews, id=review_id)
        reviews = get_object_or_404(title.reviews, id=review_id)
        serializer.save(reviews=reviews, author=self.request.user)

    def perform_update(self, serializer):
        """Overriding the perform_update() method."""
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        title = get_object_or_404(Title, id=title_id)
        get_object_or_404(title.reviews, id=review_id)
        reviews = get_object_or_404(title.reviews, id=review_id)
        serializer.save(reviews=reviews, author=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    """Category endpoint handler."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    """Genre endpoint handler."""
    queryset = Genre.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Title endpoint handler."""
    permission_classes = (IsAdminOrReadOnly, )
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id', 'category', 'genre', 'name', 'year')
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    )


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


class CreateTokenView(APIView):
    """Create JWT token endpoint handler."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """Handle JWT token POST request."""
        username = request.data.get('username', None)
        confirmation_code = request.data.get('confirmation_code', None)

        serializer = TokenRequestSerializer(data={
            'username': username,
            'confirmation_code': confirmation_code
        })
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(User, username=username)

            if not default_token_generator.check_token(
                user, confirmation_code
            ):
                return Response(
                    'Invalid confirmation code.',
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken.for_user(user)
            response = {
                'token': str(token.access_token)
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Users endpoint handler."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = pagination.LimitOffsetPagination
    search_fields = ('username',)
    lookup_field = 'username'
    permission_classes = (IsAdmin,)

    @action(
        url_path='me',
        methods=['get'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_current_user_info(self, request):
        """Retrieve the current user profile data."""
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @get_current_user_info.mapping.patch
    def update_current_user_info(self, request):
        """Update (partial) the current user profile data."""
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
