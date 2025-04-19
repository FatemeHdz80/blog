from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm, ContactForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib import messages
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm
from django.contrib.auth.decorators import login_required



def post_list(request, tag_slug=None):
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        
    context = {"posts": posts, 'page': page, "tag": tag, "page_obj": posts}
    return render(request, 'blog/post/list.html', context)



def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, 
        slug=post, 
        status="published", 
        publish__year=year, 
        publish__month=month, 
        publish__day=day
    )
    comments = post.comments.filter(active=True)

    
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags', '-publish')[:3]

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
           new_comment = comment_form.save(commit=False)
           new_comment.post = post
           new_comment.save()
           messages.success(request, 'Your comment has been submitted successfully!')
           return HttpResponseRedirect(request.path_info)
    else:
        comment_form = CommentForm()

    context = {"post":post,
            'form':comment_form,
            'comments': comments,
            's_posts': similar_posts
            }
    return render(request, 'blog/post/detail.html', context)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="published")
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        print(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())  
            subject = f"{cd['name']} recommends you"
            message = f"{post.title} in {post_url} and {cd.get('comment')}"

            send_mail(
                subject,message,"f.hz7923@gmail.com",
                [cd['to']]
            )
            return redirect('blog:post_share', post_id=post.id)
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form})


def comment_share(request, year, month, day, post):
    post = get_object_or_404(
        Post, 
        slug=post, 
        status="published", 
        publish__year=year, 
        publish__month=month, 
        publish__day=day
    )


    if not request.user.is_authenticated:
        messages.warning(request, "You need to log in to leave a comment.")
        return HttpResponseRedirect(request.path_info)

    # ✅ اگه لاگین کرده بود:
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user 
            new_comment.save()
            messages.success(request, "Your comment has been posted.")
            return HttpResponseRedirect(request.path_info)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html', {
        "post": post,
        'form': comment_form
    })
# search view
def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='C')
            search_query = SearchQuery(query)
            results = Post.published.annotate(similar = TrigramSimilarity('title', query)).filter(similar__gt=0.1).order_by('-similar')
    return render(request, 'blog/post/search.html', {'form':form, 'query':query, 'results':results})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get("next")
            messages.success(request, "Login successful.")
            return redirect(next_url or "blog:post_list")
        else:
            messages.success(request, "❌ There was a problem logging in. Please try again.")
            return redirect("blog:login_user")
    else:   
        return render(request, 'blog/post/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out!")
    return redirect("blog:post_list")

def signup_user(request):
    form = SignupForm()

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password1)
            login(request, user)

            messages.success(request, "Welcome! Your account has been successfully created.")
            return redirect("blog:post_list")
        else:
            messages.success(request, "An error occurred during your registration!")
            return redirect("blog:signup_user")
    else:

        return render(request, 'blog/post/signup.html', {'form': form})

def about(request):
    return render(request, 'blog/post/about.html')

def contact_view(request):
    form = ContactForm()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
        
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            subject = f"Message from {name}"
            from_email = email
            to_email = "f.hz7923@gmail.com" 

            send_mail(
                subject,
                message,
                from_email,
                [to_email],
                fail_silently=False,
            )

            messages.success(request, "Your message was sent successfully!")
            return redirect('blog:contact')
        else:
            form = ContactForm()  

    return render(request, 'blog/post/contact.html', {'form': form})
