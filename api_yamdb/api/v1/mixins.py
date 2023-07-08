from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter

from .permissions import IsAdminUserOrReadOnly


class GetPosDeleteViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                          mixins.DestroyModelMixin, viewsets.GenericViewSet):
    filter_backends = (SearchFilter, )
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = [IsAdminUserOrReadOnly]
