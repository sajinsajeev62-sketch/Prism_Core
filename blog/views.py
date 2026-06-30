# blog/views.py
# WORKING VERSION - Copy this ENTIRE file

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Post, Comment, Bookmark, Profile
from .forms import UserRegisterForm, PostForm, CommentForm, ProfileForm


# HOME PAGE - SIMPLE VERSION
def home(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>BlogHub</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container { 
                background: white; 
                padding: 3rem; 
                border-radius: 10px; 
                text-align: center; 
                max-width: 600px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            h1 { 
                color: #667eea; 
                font-size: 2.5rem;
                margin-bottom: 1rem;
            }
            p { 
                color: #666; 
                font-size: 1.1rem; 
                margin-bottom: 2rem;
                line-height: 1.6;
            }
            .buttons {
                display: flex;
                gap: 1rem;
                justify-content: center;
                flex-wrap: wrap;
                margin-bottom: 2rem;
            }
            .btn { 
                padding: 0.8rem 2rem; 
                background: #667eea; 
                color: white; 
                border: none; 
                border-radius: 5px;
                cursor: pointer; 
                text-decoration: none; 
                display: inline-block; 
                font-weight: bold;
                font-size: 1rem;
                transition: background 0.3s;
            }
            .btn:hover { background: #764ba2; }
            .btn-secondary { background: #6c757d; }
            .btn-secondary:hover { background: #5a6268; }
            .status { 
                background: #e8f5e9; 
                color: #2e7d32; 
                padding: 1.5rem; 
                border-radius: 5px;
                border-left: 4px solid #2e7d32;
            }
            .status p { 
                margin: 0.5rem 0;
                color: #2e7d32;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📝 Welcome to BlogHub</h1>
            <p>A beautiful blogging platform built with Django, HTML, and CSS.<br>
            Create an account and start sharing your thoughts!</p>
            
            <div class="buttons">
                <a href="/register/" class="btn">📝 Register</a>
                <a href="/login/" class="btn btn-secondary">🔓 Login</a>
                <a href="/admin/" class="btn btn-secondary">⚙️ Admin</a>
            </div>
            
            <div class="status">
                <p>✅ Server is running successfully!</p>
                <p>🎉 Your Django blog app is live and ready!</p>
                <p style="font-size: 0.9rem; margin-top: 1rem;">Click Register to create your first account</p>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


# AUTH VIEWS
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            messages.success(request, 'Account created!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

# POST VIEWS
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    
    is_liked = post.likes.filter(id=request.user.id).exists() if request.user.is_authenticated else False
    is_bookmarked = Bookmark.objects.filter(user=request.user, post=post).exists() if request.user.is_authenticated else False
    
    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'is_liked': is_liked,
        'is_bookmarked': is_bookmarked
    })

@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form, 'title': 'Create Post'})

@login_required(login_url='login')
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('post-detail', pk=post.pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form, 'title': 'Edit Post'})

@login_required(login_url='login')
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('post-detail', pk=post.pk)
    
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'post_confirm_delete.html', {'post': post})

@login_required(login_url='login')
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post-detail', pk=post.pk)

@login_required(login_url='login')
def bookmark_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    bookmark = Bookmark.objects.filter(user=request.user, post=post).first()
    if bookmark:
        bookmark.delete()
    else:
        Bookmark.objects.create(user=request.user, post=post)
    return redirect('post-detail', pk=post.pk)

def search_posts(request):
    query = request.GET.get('q', '')
    posts = Post.objects.all()
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(author__username__icontains=query))
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    return render(request, 'search_results.html', {'posts': posts_page, 'query': query})

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    posts = user.posts.all().order_by('-created_at')
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'profile': profile, 'user': user, 'posts': posts_page})

@login_required(login_url='login')
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

@login_required(login_url='login')
def my_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user).order_by('-created_at')
    posts = [bookmark.post for bookmark in bookmarks]
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    return render(request, 'bookmarks.html', {'posts': posts_page})