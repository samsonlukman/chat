from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.register, name="register"),
    path('get_messages', views.get_messages, name="get_messages"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout")
]