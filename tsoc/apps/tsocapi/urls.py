from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, DetailsView, UserViewSet

#router = DefaultRouter(trailing_slash=False)
router = SimpleRouter()
router.register(r'users', UserViewSet)

urlpatterns = {
    url(r'^', include(router.urls)),
    url(r'^posts/$', CreateView.as_view(), name="post_create"),
    url(r'^posts/(?P<pk>[0-9]+)/$', DetailsView.as_view(), name="post_details"),
    # path('users/<int:user_id>', UserListCreateView.as_view(), name="user"),
    # url(r'^users/(?P<pk>[0-9]+)/$', UserListCreateView.as_view(), name="user"),

}

urlpatterns = format_suffix_patterns(urlpatterns)
