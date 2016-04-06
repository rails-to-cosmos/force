from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser

from django.contrib.auth.models import User
from serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
