from django.urls import path

from apps.blog.views import PostListView, PostDetailView, PostFromCategory, PostCreateView

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('post/create/', PostCreateView.as_view(), name = 'post_create'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', PostFromCategory.as_view(), name='post_by_category' ),

]