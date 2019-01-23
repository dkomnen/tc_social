from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

router = SimpleRouter()
router.register(r'users', UserViewSet)

urlpatterns = {
    url(r'^users/?$', RegistrationAPIView.as_view()),
    url(r'^users/login/?$', LoginAPIView.as_view()),
    url(r'^posts/$', PostListView.as_view(), name="post_details"),
    url(r'^posts/(?P<pk>[0-9]+)/$', PostDetailsView.as_view(), name="post_details"),
    url(r'^users/(?P<user_pk>[0-9]+)/posts/$', UserPostCreateView.as_view(), name="user_post_create"),
    url(r'^users/(?P<user_pk>[0-9]+)/posts/(?P<pk>[0-9]+)/$', UserPostDetailsView.as_view(), name="user_post_details"),
    url(r'^users/(?P<user_pk>[0-9]+)/posts/(?P<post_pk>[0-9]+)/like/$', UserPostLikesCreateView.as_view(),
        name="user_post_like_create"),
    url(r'^users/(?P<user_pk>[0-9]+)/posts/(?P<post_pk>[0-9]+)/unlike/$', UserPostLikesDeleteView.as_view(),
        name="user_post_like_delete"),
    url(r'^users/(?P<user_pk>[0-9]+)/likes/$', UserLikesDetailsView.as_view(),
        name="user_likes_details"),

}

urlpatterns = format_suffix_patterns(urlpatterns)
