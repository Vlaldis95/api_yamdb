from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (APIGetToken, APISignup, CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet, UsersViewSet)

router = SimpleRouter()

router.register('users', UsersViewSet, basename='users')

router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register(r'titles/(?P<title_id>/d+)/reviews/',
                   ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>/d+)/comments',
    CommentViewSet, basename='comments')

urlpatterns = [
    path('auth/token/', APIGetToken.as_view(), name='get_token'),
    path('auth/signup/', APISignup.as_view(), name='signup'),
    path('', include(router.urls)),
]
