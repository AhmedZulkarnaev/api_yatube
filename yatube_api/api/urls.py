from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, GroupViewSet, PostViewSet

API_VERSION = 'v1'

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet)
router.register('groups', GroupViewSet)

urlpatterns = [
    path(f'api/{API_VERSION}/api-token-auth/', views.obtain_auth_token),
    path(f'api/{API_VERSION}/', include(router.urls))
]
