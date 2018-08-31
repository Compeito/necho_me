from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'
urlpatterns = [
    path('logout/', auth_views.logout, {'template_name': 'account/logout.html'}, name='logout'),
    path('redirect/', views.login_after_redirect),
    path('settings/', views.user_settings)
]
