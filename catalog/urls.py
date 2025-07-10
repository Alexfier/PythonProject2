from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home
from django.conf import settings
from django.conf.urls.static import static
from . import views

from catalog.views import products_list, products_detail

app_name = CatalogConfig.name

urlpatterns = ([
                   path("", home, name="home"),
                   path("contacts/", views.contact, name="contacts"),
                   path('products_list', products_list, name='products_list'),
                   path('products/<int:pk>/', products_detail, name='products_detail')
               ]
               + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))