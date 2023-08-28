from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from pytils.translit import slugify

from blog.forms import ArticleForm
from blog.models import Article


class BlogCreateView(CreateView):
    """
    Создает новый экземпляр модели "Статья"
    """
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('blog:list')

    # Динамически формируем slug name
    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class BlogListView(ListView):
    """
    Выводит все статьи на страницу
    """
    model = Article

    # Выводит только активные статьи
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publication=True)
        return queryset


class BlogUpdateView(UpdateView):
    """
    Позволяет изменить существующие статьи
    """
    model = Article
    form_class = ArticleForm

    # Динамически формируем slug name
    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    # После обнавления перенаправляет на статью
    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class BlogDetailView(DetailView):
    """
    Выводит статью целиком
    """
    model = Article

    # Счетчик просмотров
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    """
    Удаляет элемент
    """
    model = Article
    success_url = reverse_lazy('blog:list')
