from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    """
    User model representing a user in the system.
    Attributes:
        is_admin (bool): Indicates whether the user is an admin or not. Default is False.
    """
    is_admin = models.BooleanField(default=False)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    image_id = models.IntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on image {self.image_id}'


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    image = CloudinaryField('image')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(Comment, blank=True)

    def __str__(self):
        return f'Image {self.id} by {self.user.username}'

    def get_comments(self):
        return Comment.objects.filter(image_id=self.id)

    def get_comments_count(self):
        return Comment.objects.filter(image_id=self.id).count()

    def get_likes_count(self):
        return Like.objects.filter(image_id=self.id).count()
