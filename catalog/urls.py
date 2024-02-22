from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import product_views, blog_views,contact_views

app_name = CatalogConfig.name

urlpatterns = [

    path('contacts/', contact_views.ContactsListView.as_view(), name='contacts'),

    path('', product_views.ProductsListView.as_view(), name='home'),

    path('product/<int:pk>/', product_views.ProductDetailView.as_view(), name='product'),
    # кэширование контроллера
    # path('product/<int:pk>/', cache_page(60)(product_views.ProductDetailView.as_view()), name='product'),

    path('create_product/', product_views.ProductCreateView.as_view(), name='create_product'),
    path('update_product/<int:pk>', product_views.ProductUpdateView.as_view(), name='update_product'),
    path('delete_product/<int:pk>', product_views.ProductDeleteView.as_view(), name='delete_product'),

    path('blog/', blog_views.BlogView.as_view(), name='blog'),
    path('blog/create_post/', blog_views.BlogPostCreateView.as_view(), name='create_post'),
    path('blog/post/<int:year>/<int:month>/<int:day>/<slug:slug>/',
         blog_views.BlogPostDetailView.as_view(), name='post'),
    path('blog/update_post/<int:year>/<int:month>/<int:day>/<slug:slug>/',
         blog_views.BlogPostUpdateView.as_view(), name='update_post', ),
    path('blog/delete_post/<int:year>/<int:month>/<int:day>/<slug:slug>/',
         blog_views.BlogPostDeleteView.as_view(), name='delete_post'),

]
