from django import template
from blog.models import Post
from django.utils import timezone

register = template.Library()

@register.inclusion_tag('website/index-blog.html')
def display_latest_posts():
    current_time = timezone.now()
    posts=Post.objects.filter(status=1,published_date__lte=current_time).order_by('-published_date')[0:6]
    return {'posts':posts}  