from django.urls import URLPattern, path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', views.setting, name='settings'),
    path('upload/', views.upload, name='upload'),
    path('like_post/', views.like_post, name='like_post'),
    path('profile/<str:un>/', views.Profile, name='profile'),
    path('follow/', views.follow, name='follow'),
    path('search/', views.search, name='search'),
]