# blog/urls.py
# Pure Django - No JavaScript Required

from django.urls import path
from . import views

urlpatterns = [
    # Home & Auth
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Posts
    path('post/new/', views.create_post, name='create-post'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit-post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete-post'),
    
    # Likes & Bookmarks (Form Submissions)
    path('post/<int:pk>/like/', views.like_post, name='like-post'),
    path('post/<int:pk>/bookmark/', views.bookmark_post, name='bookmark-post'),
    
    # Search
    path('search/', views.search_posts, name='search'),
    
    # Profiles
    path('profile/<str:username>/', views.user_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    path('bookmarks/', views.my_bookmarks, name='bookmarks'),
]