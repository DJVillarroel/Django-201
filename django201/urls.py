from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

from feed import urls as feed_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(feed_urls, namespace="feed")),
    path("", include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
