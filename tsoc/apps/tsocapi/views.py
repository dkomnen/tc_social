from django.shortcuts import render
from rest_framework import generics, viewsets, status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .serializers import PostSerializer, UserSerializer, UserPostLikesSerializer, RegistrationSerializer, \
    LoginSerializer
from .models import Post, UserPostLikes, User
from .renderers import UserJSONRenderer
from .services.emailhunter import hunter_client
from .services.clearbit import clearbit_client
from django.conf import settings


# Create your views here.

class RegistrationAPIView(views.APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer_data = request.data.get('user', {})
        if settings.CLEARBIT_ACTIVE:
            enrichment_data = clearbit_client.clearbit_data_enrichment(email=serializer_data.get('email', {}))
            if enrichment_data is not None:
                print(enrichment_data)
                serializer_data["first_name"] = enrichment_data['person']['name']['givenName']
                serializer_data["last_name"] = enrichment_data['person']['name']['familyName']

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=serializer_data)

        serializer.is_valid(raise_exception=True)
        if settings.HUNTER_ACTIVE:
            if not hunter_client.is_email_deliverable(email=serializer_data.get('email', {})):
                return Response({"message": "Email is not valid"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(views.APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # lookup_field = 'pk'

    def create(self, request):
        serializer_context = {
            'request': request
        }
        serializer_data = request.data.get('user', {})
        enrichment_data = clearbit_client.clearbit_data_enrichment(email=serializer_data.get('email', {}))
        if enrichment_data is not None:
            print(enrichment_data)
            serializer_data["first_name"] = enrichment_data['person']['name']['givenName']
            serializer_data["last_name"] = enrichment_data['person']['name']['familyName']

        serializer = self.serializer_class(
            data=serializer_data,
            context=serializer_context
        )

        serializer.is_valid(raise_exception=True)
        if not hunter_client.is_email_deliverable(email=serializer_data.get('email', {})):
            return Response({"message": "Email is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
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
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserPostCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, user_pk):
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

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, user_pk):
        queryset = Post.objects.filter(user=user_pk).all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


class UserPostDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserPostLikesCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
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


class UserPostLikesDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UserPostLikes.objects.all()
    serializer_class = UserPostLikesSerializer
    lookup_field = 'user_pk'

    def destroy(self, request, user_pk, post_pk):
        queryset = UserPostLikes.objects.get(user=user_pk, post=post_pk).delete()
        return Response(status=status.HTTP_200_OK)


class UserLikesDetailsView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UserPostLikes.objects.all()
    serializer_class = PostSerializer

    def list(self, request, user_pk):
        queryset = UserPostLikes.objects.filter(user=user_pk).all()
        serializer = UserPostLikesSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
