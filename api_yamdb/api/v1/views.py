from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from .utils import send_confirmation_code

from reviews.models import Category, Genre, Review, Title, User, Comment

from .filters import TitleFilter
from .mixins import GetPosDeleteViewSet
from .permissions import IsSuperUserOrIsAdminOnly, IsAdminUserOrReadOnly
from .permissions import ReviewCommentPermission
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleSerializer, GetTitleSerializer,
                          UserCreateSerializer, UserGetTokenSerializer,
                          UserSerializer)


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        if request.user.is_anonymous:
            confirmation_code = default_token_generator.make_token(user)
            send_confirmation_code(
                email=user.email,
                confirmation_code=confirmation_code
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserGetTokenViewSet(mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserGetTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = UserGetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            message = {'confirmation_code': 'Код подтверждения невалиден'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)


class UserViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUserOrIsAdminOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch', 'delete'],
        url_path=r'(?P<username>[\w.@+-]+)',
        url_name='get_user'
    )
    def get_user_by_username(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_me_data(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetTitleSerializer
        return TitleSerializer


class CategoryViewSet(GetPosDeleteViewSet):
    queryset = Category.objects.all()
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = "slug"
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = CategorySerializer


class GenreViewSet(GetPosDeleteViewSet):
    queryset = Genre.objects.all()
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = "slug"
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = GenreSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (ReviewCommentPermission,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        comments = Comment.objects.filter(review_id=review_id)
        return comments

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        comment_id = self.kwargs.get('pk')
        author = Comment.objects.get(pk=comment_id).author
        serializer.save(author=author, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (ReviewCommentPermission,)

    def get_queryset(self):
        reviews = Review.objects.filter(title_id=self.kwargs.get('title_id'))
        return reviews

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review_id = self.kwargs.get('pk')
        author = Review.objects.get(pk=review_id).author
        serializer.save(author=author, title=title)
