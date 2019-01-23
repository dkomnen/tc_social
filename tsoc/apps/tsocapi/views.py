from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .serializers import PostSerializer, UserSerializer, UserPostLikesSerializer
from .models import Post, UserPostLikes
from django.contrib.auth.models import User
from .services.emailhunter import hunter_client
from .services.clearbit import clearbit_client


# Create your views here.

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # lookup_field = 'pk'

    def create(self, request):
        serializer_context = {
            'request': request
        }
        serializer_data = request.data.get('user', {})
        # enrichment_data = clearbit_client.clearbit_data_enrichment(email=serializer_data.get('email', {}))
        # if enrichment_data is not None:
        #     print(enrichment_data)
        #     serializer_data["first_name"] = enrichment_data['person']['name']['givenName']
        #     serializer_data["last_name"] = enrichment_data['person']['name']['familyName']

        serializer = self.serializer_class(
            data=serializer_data,
            context=serializer_context
        )

        serializer.is_valid(raise_exception=True)
        # if not hunter_client.is_email_deliverable(email=serializer_data.get('email', {})):
        #     return Response({"message": "Email is not valid"},status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        # serializer_context = {'request': request}
        # page = self.paginate_queryset(self.get_queryset())
        #
        # serializer = self.serializer_class(
        #     page,
        #     context=serializer_context,
        #     many=True
        # )
        #
        # return self.get_paginated_response(serializer.data)
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        serializer_context = {'request': request}

        try:
            serializer_instance = self.queryset.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound('A user with this id does not exist.')

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, slug):
        serializer_context = {'request': request}

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except User.DoesNotExist:
            raise NotFound('An user with this slug does not exist.')

        serializer_data = request.data.get('user', {})

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context,
            data=serializer_data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserPostCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, request, user_pk):
        serializer_context = {
            'request': request
        }
        serializer_data = {'user': user_pk, 'post_text': request.data.get('post_text', {})}

        serializer = self.serializer_class(
            data=serializer_data,
            context=serializer_context
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()


class UserPostDetailsView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserPostLikesCreateView(generics.ListCreateAPIView):
    queryset = UserPostLikes.objects.all()
    serializer_class = UserPostLikesSerializer
    lookup_field = 'user_pk'

    def create(self, request, user_pk, post_pk):
        serializer_context = {
            'request': request
        }
        serializer_data = {'user': user_pk, 'post': post_pk}

        serializer = self.serializer_class(
            data=serializer_data,
            context=serializer_context
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLikesDetailsView(generics.ListAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = UserPostLikes.objects.all()
    serializer_class = PostSerializer

    def list(self, request, user_pk):
        queryset = UserPostLikes.objects.filter(user=user_pk).all()
        serializer = UserPostLikesSerializer(queryset, many=True)
        return Response(serializer.data)
