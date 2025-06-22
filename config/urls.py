from django.contrib import admin
from django.urls import path, include

from catalog.views import home

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls', namespace='catalog'))
]