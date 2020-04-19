"""newscraper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import views as a_v
from django.contrib import admin
from django.urls import path, include
from account.views import (home, registration, logout_view, login_view, account_view, account_delete_view,account_delete_done_view,favourite,checkFavorite  )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('favourite/', favourite, name='favourite'),
    path('register/', registration, name="register"),
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name='login'),
    path('account/', account_view, name='account'),
    path('delete/', account_delete_view, name="account-delete"),
    path('delete-done/', account_delete_done_view, name="account-delete-done"),
    path('favorite/<pk>/', checkFavorite, name="favourite2"),


    # Password change links
    path('password_change/done/',
         a_v.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', a_v.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),




]
