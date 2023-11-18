from django.shortcuts import render
from .models import Post,Comment
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.urls import reverse 
from django.http import QueryDict




def blog_view(request, **kwargs):
    current_time = timezone.now()
    posts = Post.objects.filter(status=True, published_date__lte=current_time).order_by('-published_date')
    if kwargs.get('cat_name'):
        posts = posts.filter(category__name=kwargs['cat_name'])
    if kwargs.get('username'):
        posts = posts.filter(author__username=kwargs['username'])

    if kwargs.get('tag_name'):
        posts = posts.filter(tags__name=kwargs['tag_name'])
    # Fetch tags for each post and include them in the context

    for post in posts:
        post.tags = post.tags.all()

    paginator = Paginator(posts, 3)

    try:
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
    except EmptyPage:
        posts = paginator.get_page(1)
    except PageNotAnInteger:
        posts = paginator.get_page(1)

    context = {'posts': posts,}
    return render(request, 'blog/blog-home.html', context)

def blog_single(request, pid):
    current_time = timezone.now()
    post = get_object_or_404(Post, pk=pid, status=True, published_date__lte=current_time)
    all_posts = Post.objects.filter(status=True, published_date__lte=current_time).order_by('-published_date')
    comments = Comment.objects.filter(post=post, approved=True).order_by('-created_date')
    current_index = list(all_posts).index(post)
    next_post = all_posts[current_index - 1] if current_index > 0 else None
    previous_post = all_posts[current_index + 1] if current_index < len(all_posts) - 1 else None
    post.counted_views += 1
    post.save()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        
        if request.user.is_authenticated:
            initial_data = {
                'name': request.user.username,
                'email': request.user.email,
            }
            combined_data = {**initial_data, **request.POST}
            comment_form = CommentForm(combined_data)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Submitted correctly')
            return redirect(request.path_info)
        else:
            messages.error(request, 'Oops, there was an error in the form submission!') 
    else:
        comment_form = CommentForm()

    return render(request, 'blog/blog-single.html', {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
        'comments': comments,
        'comment_form': comment_form,
    })

def blog_search(request):
    query = request.GET.get('s')  # Retrieve the 's' parameter from the GET request
    posts = Post.objects.filter(status=1)

    if query:
        # Use 'icontains' for case-insensitive search in both title and content
        posts = posts.filter(title__icontains=query) | posts.filter(content__icontains=query)

    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)
