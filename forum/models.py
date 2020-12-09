from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Topic(models.Model):
    title = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,  null=True)
    published_date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    slug = AutoSlugField(populate_from='title', unique=True, null=True)
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_pinned', '-published_date']

    def __str__(self):
        return f'{self.title} by {self.user}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("reply_list", kwargs={"slug": self.slug})


class Reply(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,  null=True)

    published_date = models.DateTimeField(auto_now_add=True)
    content = RichTextUploadingField(config_name='reply_box', max_length=6000)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    flags = models.ManyToManyField(User, blank=True, related_name='flags')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.topic.title}'

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_flags(self):
        return self.flags.count()
