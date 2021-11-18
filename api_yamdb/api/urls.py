from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, create_token,
                    sign_up)

router = DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='reviews'),
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='title')
router.register('users', UserViewSet, basename='users')

auth_urls = [
    path('signup/', sign_up, name='signup'),
    path('token/', create_token, name='token'),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_urls))
]
