from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post
from django.utils import timezone



class LatestEntriesFeed(Feed):

    title = "Blog Feed"
    link = "/rss/feed"
    description = "Updates on changes and additions to police beat central."

    def items(self):
        current_time = timezone.now()
        return  Post.objects.filter(status=True, published_date__lte=current_time).order_by('-published_date')



    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content[:100]

    # # item_link is only needed if NewsItem has no get_absolute_url method.
    # def item_link(self, item):
    #     return reverse("news-item", args=[item.pk])