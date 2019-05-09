from django.contrib import admin
from django.urls import path

from estimation.views import estimate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/estimate/', estimate)
]
