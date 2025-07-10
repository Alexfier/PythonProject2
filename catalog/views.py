from django.shortcuts import render
from .models import Blog
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


# Create your views here.

class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)


class BlogCreateView(CreateView):
    model = Blog
    fields = ['title', 'preview', 'content', 'is_published']
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        form.instance.is_published = True  # публикуем автоматически
        return super().form_valid(form)

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Увеличиваем количество просмотров
        self.object.views_count += 1
        self.object.save(update_fields=['views_count'])
        return super().get(request, *args, **kwargs)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ["title", "created_at", "preview", "content"]
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog_list')

    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog_list')