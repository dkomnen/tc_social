from django.test import TestCase
from .models import Post, UserPostLikes
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


# Create your tests here.

class ModelTestCase(TestCase):

    def setUp(self):
        """Define the test client and other test variables."""
        self.user = User(first_name="David", last_name="Komljenovic", username="WhiteSeraph")
        self.user.save()
        self.post = Post(post_text="This is a test post!", user=self.user)

    def test_model_can_create_a_post(self):
        """Test the post model can create a post."""
        old_count = Post.objects.count()
        self.post.save()
        new_count = Post.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_create_a_user(self):
        self.test_user = User(first_name="David1", last_name="Komljenovic", username="WhiteSeraph1")
        old_count = User.objects.count()
        self.test_user.save()
        new_count = User.objects.count()
        self.assertNotEqual(old_count, new_count)


class ViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User(first_name="David", last_name="Komljenovic", username="WhiteSeraph")
        self.user.save()
        self.post = Post(post_text="This is a test post!", user=self.user)
        self.post.save()

    def test_api_can_create_a_post(self):
        self.post_data = {"post_text": "This is a test post!", "user": self.user.id}
        self.response = self.client.post(
            reverse('create'),
            self.post_data,
            format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_post(self):
        """Test the api can get a given post."""
        post = Post.objects.get()
        response = self.client.get(
            reverse('details', kwargs={'pk': post.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, post)

    def test_api_can_update_post(self):
        """Test the api can update a given post."""
        post = Post.objects.get()
        change_post = {'name': 'Something new'}
        res = self.client.put(
            reverse('details', kwargs={'pk': post.id}),
            change_post, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_post(self):
        """Test the api can delete a post."""
        post = Post.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': post.id}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
