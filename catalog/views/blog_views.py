from django.contrib.auth import mixins
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views import generic

from catalog.forms import BlogForm
from catalog.models import Post
from catalog.services import sendmail



class BlogPostCreateView(mixins.PermissionRequiredMixin, generic.CreateView):
    permission_required = 'catalog.add_post'
    model = Post
    form_class = BlogForm
    success_url = reverse_lazy('catalog:blog')
    extra_context = {
        'title': 'Создание статьи'
    }

    def form_valid(self, form):
        if form.is_valid:
            fields = form.save(commit=False)
            string = fields.title.translate(
                str.maketrans("абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                              "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"))
            fields.slug = slugify(string)
            fields.save()
        return super().form_valid(form)


class BlogView(generic.ListView):
    model = Post
    template_name = 'catalog/blog.html'
    extra_context = {
        'title': 'Блог'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(published=True)
        return queryset


class BlogPostDetailView(generic.DetailView):
    model = Post

    def get_object(self, queryset=None):  # добавление одного просмотра
        post = super().get_object()
        post.add_view()
        if post.views == 100:
            sendmail(
                f'Поздравляю, статья "{post.title}" набрала {post.views} просмотров',
                ('alex77bel@yandex.ru', )
            )
        post.save()
        return post

    def get_context_data(self, **kwargs):  # получение 'title'
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Просмотр статьи'
        return context_data


class BlogPostUpdateView(mixins.PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'catalog.change_post'
    model = Post
    form_class = BlogForm
    extra_context = {
        'title': 'Изменить статью'
    }

    def get_success_url(self):
        return reverse('catalog:post', args=[*self.kwargs.values()])


class BlogPostDeleteView(mixins.PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'catalog.delete_post'
    model = Post
    template_name = 'catalog/confirm_delete.html'
    extra_context = {
        'title': 'Удаление'
    }
    success_url = reverse_lazy('catalog:blog')
