from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import (CategoryViewSet, CommentsViewSet, CreateTokenView,
                    GenreViewSet, ReviewViewSet, SignUpView, TitleViewSet)

router = DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='reviews'),
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='title')
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', CreateTokenView.as_view(), name='token'),
]
