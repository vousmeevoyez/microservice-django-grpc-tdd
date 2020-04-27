from rest_framework.viewsets import ModelViewSet


class UserOwnViewSet(ModelViewSet):
    """
        GET POST PUT PATCH DELETE /stores/
        _____________________
        base model viewset class to return only their own data
    """

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(user=self.request.user)
