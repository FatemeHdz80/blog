from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post
from django.template.defaultfilters import truncatewords, safe

class LatestPostFeed(Feed):
    title = 'My Blog'
    description = "This is my post description"

    def link(self):
        return reverse('blog:post_list')  

    def items(self):
        return Post.published.all()[:5]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return safe(truncatewords(item.body, 30))
