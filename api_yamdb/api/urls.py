from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignUpView

router = DefaultRouter()

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
]
