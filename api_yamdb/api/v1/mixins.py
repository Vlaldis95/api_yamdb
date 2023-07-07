from rest_framework import mixins, viewsets


class GetPosDeleteViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                          mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass
