from django.urls import path

from . import views

app_name = "profiles"

urlpatterns = [
    path("<str:username>/", views.ProfileDetailView.as_view(), name="detail"),
    path("<str:username>/follow/", views.FollowView.as_view(), name="follow"),
    path('settings/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
]