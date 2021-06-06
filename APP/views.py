from django.db import connection
from rest_framework import generics
from rest_framework import permissions
from APP import serializers
from django.contrib.auth.models import User


from APP.models import Post
from APP.permissions import IsOwnerOrReadOnly


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.RegisterSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class PostListView(generics.ListAPIView):
    """Endpoint for retrieve all posts
    """
    queryset = Post.objects.select_related('owner',)
    serializer_class = serializers.PostSerializer

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        print(f'Queries Counted: {len(connection.queries)}')
        return response


class PostCreateView(generics.CreateAPIView):
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer


class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )


class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )





