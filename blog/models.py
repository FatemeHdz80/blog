from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext as _
from taggit.managers import TaggableManager


class PublisheManager(models.Manager):
    def get_queryset(self):
        return super(PublisheManager, self).get_queryset().filter(status='published')
    

class Post(models.Model):
    STATUS = (
        ("draft", 'Draft'),
        ("published", 'Published')
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    title = models.CharField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS, default='draft')
    objects = models.Manager()
    published = PublisheManager()
    tags = TaggableManager()
    picture_url = models.URLField(max_length=1000)

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

 
    def __str__(self):
        return self.slug
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, null=True, blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

        def __str__(self):
            return f"comment by {self.name} on {self.post}"
    
