from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.core.paginator import Paginator
from django.views import View
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from .filters import NewsFilter
from .forms import PostForm, RegisterForm, LoginForm

# Create your views here.

class PostList(ListView):
    model = Post
    template_name = 'news.html' 
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    paginate_by = 2
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'details_news.html' 
    context_object_name = 'new_s'
    queryset = Post.objects.filter(type='NW')

class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'add_post.html'
    form_class = PostForm
    permission_required = ('news.add_post',)


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'post_update.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id_id = self.kwargs.get('pk')
        return Post.objects.get(pk=id_id)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.delete_post',)


class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())

        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)
    
class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'sign/signup.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get_or_create(name='common')[0]
        user.groups.add(group)
        user.save()
        return super().form_valid(form)
    
class LoginView(FormView):
    model = User
    form_class = LoginForm
    template_name = 'sign/login.html'
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


@login_required
def get_author(request):
    user = request.user
    Author.objects.create(authorUser=user)
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'account/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name = 'premium').exists()
        return context

@login_required
def upgrade_me(request):
   user = request.user
   premium_group = Group.objects.get(name='authors')
   if not request.user.groups.filter(name='authors').exists():
       premium_group.user_set.add(user)
   return redirect('/')
