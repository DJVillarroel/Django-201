from typing import Any
from django.contrib.auth.models import User
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest
from feed.models import Post
from followers.models import Follower
from .forms import ProfileUpdateForm
from django.shortcuts import render, redirect

class ProfileDetailView(DetailView):
    http_method_names = ["get"]
    template_name = "profiles/detail.html"
    model = User
    context_object_name = "user" 
    slug_field = "username"
    slug_url_kwarg = "username"
    
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(author=user).count()
        context['total_followers'] = Follower.objects.filter(following=user).count() #Filtrar todos los usuarios que sigan a user, contarlos
        context['total_follows'] = Follower.objects.filter(followed_by=user).count() #Filtrar todos los usuarios a los que sigue user, contarlos
        if self.request.user.is_authenticated:
            context['you_follow'] = Follower.objects.filter(following=user, followed_by=self.request.user).exists()
        return context
    
class FollowView(LoginRequiredMixin, View):
    http_method_names = ["post"]
    
    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        
        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest("Missing data")
            
        try:
            other_user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return HttpResponseBadRequest("Missing user")
        
        if data['action'] == 'follow':
            #follow
            follower, created = Follower.objects.get_or_create(
                followed_by = request.user,
                following = other_user
            )
        else:
            #unfollow
            try:
                follower = Follower.objects.get(
                    followed_by = request.user,
                    following = other_user
                )
            except Follower.DoesNotExist:
                follower= None
            
            if follower:
                follower.delete() 
            
            
        return JsonResponse({
            'done': True,
            'wording': 'Unfollow' if data['action'] == 'follow' else 'Follow'
        })
        
class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'profiles/settings.html'
    form_class = ProfileUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user.profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profiles:detail', username=request.user.username)
        return render(request, self.template_name, {'form': form})