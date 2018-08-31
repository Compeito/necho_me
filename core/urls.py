from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.top),
    path('home/', views.home, name='home'),
    path('<slug:slug>/', views.detail),
    path('del/<slug:slug>/', views.delete),
    path('u/<slug:username>/', views.UserPage.as_view()),
    path('favicon.ico', views.favicon),
]
