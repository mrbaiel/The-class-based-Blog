from django.urls import path

from apps.blog.views import PostListView, PostDetailView, PostFromCategory, PostCreateView, PostUpdateView

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('post/create/', PostCreateView.as_view(), name = 'post_create'),
    path('category/<slug:slug>/update/', PostUpdateView.as_view(), name = 'post_update'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', PostFromCategory.as_view(), name='post_by_category' ),

]
