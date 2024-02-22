from django.contrib.auth import mixins
from django.forms import inlineformset_factory
from django.http import Http404
from django.urls import reverse_lazy
from django.views import generic
from catalog.models import Product, Version

from catalog.forms import ProductForm, VersionForm
from catalog.services import get_category_cached

PRODUCTS_PER_PAGE = 6


class ProductsListView(mixins.LoginRequiredMixin, generic.ListView):
    queryset = Product.published.all()
    paginate_by = PRODUCTS_PER_PAGE
    extra_context = {
        'title': 'Продукты'
    }


class ProductDetailView(mixins.LoginRequiredMixin, generic.DetailView):
    queryset = Product.published.all()
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Просмотр продукта'
        context_data['category'] = get_category_cached(self.object.pk)
        return context_data


class ProductCreateView(mixins.PermissionRequiredMixin, generic.CreateView):
    permission_required = 'catalog.add_product'
    queryset = Product.published.all()
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')
    extra_context = {
        'title': 'Создание продукта'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        version_formset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        context_data['formset'] = version_formset()

        if self.request.method == 'POST':
            context_data['formset'] = version_formset(self.request.POST)
        else:
            context_data['formset'] = version_formset()
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        if form.is_valid():
            fields = form.save(commit=False)
            fields.user = self.request.user
            fields.save()
        return super().form_valid(form)


class ProductUpdateView(mixins.PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'catalog.change_product'
    queryset = Product.published.all()
    form_class = ProductForm
    extra_context = {
        'title': 'Изменение продукта'
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404('Изменять может только владелец продукта')
        return self.object

    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        version_formset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        context_data['formset'] = version_formset()

        if self.request.method == 'POST':
            context_data['formset'] = version_formset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = version_formset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(mixins.PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'catalog.delete_product'
    queryset = Product.published.all()
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    extra_context = {
        'title': 'Удаление'
    }
