from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import detail_route, list_route

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

    @list_route(methods=['get'])
    def current(self, request, format):
        queryset = User.objects.filter(id=request.user.id)
        serializer = UserSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
