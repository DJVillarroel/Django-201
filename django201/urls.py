from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

from profiles import urls as profiles_urls
from feed import urls as feed_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(feed_urls, namespace="feed")),
    path("profile/", include(profiles_urls, namespace="profiles")),
    path("", include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
