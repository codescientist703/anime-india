from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from easy_thumbnails.fields import ThumbnailerImageField


class Profile(models.Model):
    choices = (
        ('Action', 'Action'),
        ('Adventure', 'Adventure'),
        ('Fantasy', 'Fantasy'),
        ('Romance', 'Romance'),
        ('Historical', 'Historical'),
        ('Sci-fi', 'Sci-fi'),
        ('Seinen', 'Seinen'),
        ('Shounen', 'Shounen'),
        ('Mystery', 'Mystery'),
        ('Ecchi', 'Ecchi'),
        ('Sports', 'Sports'),
        ('Psychological', 'Psychological'),
        ('Supernatural', 'Supernatural'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about_me = models.TextField(blank=True, null=True)
    location = models.CharField(blank=True, max_length=100, null=True)
    favourite_anime = models.CharField(blank=True, max_length=100, null=True)
    favourite_genres = MultiSelectField(
        choices=choices, blank=True, null=True)
    image = ThumbnailerImageField(
        default="avatar.jpg", null=True, blank=True, upload_to="users/", resize_source=dict(size=(200, 200), quality=40, crop=True))

    def __str__(self):
        return self.user.username
