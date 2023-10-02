from django.urls import path, include
from django.views.decorators.cache import cache_page
from .views import *
from .views import upgrade_me

urlpatterns = [
    path('', cache_page(10)(PostList.as_view()), name='news'),
    path('<int:pk>', PostDetail.as_view(), name='new_s'),
    path('add', PostCreateView.as_view(), name='add_post'),
    path('update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('search', SearchList.as_view(), name='search'),
    path('login/', LoginView.as_view(template_name='login_page.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout_page.html'), name='logout'),
    path('', IndexView.as_view(), name='index'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('getauthor/', get_author, name='getauthor'),
    path('upgrade/', upgrade_me,name='upgrade')
]