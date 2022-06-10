 
from django.urls import path
# we using auth views for login and logout // and don't mix with the real views
from django.contrib.auth import views as auth_views
from django.urls import URLPattern
from . import views

app_name='accounts'

urlpatterns =[ 
    path('login',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout',auth_views.LogoutView.as_view(),name='logout'),
    path('signup',views.SignUp.as_view(),name='signup')
]