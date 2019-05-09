from django.contrib import admin
from django.urls import path

from estimation.views import index, estimate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('estimate/', estimate)
]
