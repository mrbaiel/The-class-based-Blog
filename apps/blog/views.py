from lib2to3.fixes.fix_input import context

from django.views.generic import ListView, DetailView

from django.shortcuts import render
from django.views.generic import RedirectView
from unicodedata import category

from apps.blog.models import Post, Category


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    queryset = Post.custom.all() #Предопределили вызов модели

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class PostFromCategory(ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    category = None
    paginate_by = 6

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Post.custom.filter(category__slug=self.category.slug)
        if not queryset:
            sub_cat = Category.objects.filter(parent=self.category)
            queryset = Post.custom .filter(category__in=sub_cat)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Записи категорий: {self.category.title}'
        return context
