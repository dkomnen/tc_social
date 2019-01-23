from django.db import models
from tsoc.apps.core.models import TimestampedModel
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here

# class UserProfile(models.Model):
#     class Meta:
#         db_table = "user_profile"
#
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()


class Post(TimestampedModel):
    class Meta:
        db_table = "post"

    post_text = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # return self.post_text
        return "{}".format(self.post_text)


class UserPostLikes(TimestampedModel):
    class Meta:
        db_table = "user_post_likes"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
