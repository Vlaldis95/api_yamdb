from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserCreateViewSet,
                    UserGetTokenViewSet, UserViewSet)

router = SimpleRouter()

router.register('users', UserViewSet, basename='users')

router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

urlpatterns = [
    path('auth/token/', UserGetTokenViewSet.as_view({'post': 'create'}),
         name='token'),
    path('auth/signup/', UserCreateViewSet.as_view({'post': 'create'}),
         name='signup'),
    path('', include(router.urls)),
]
