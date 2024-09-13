"""
URL configuration for aircraft_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from tracker import views



urlpatterns = [
    path('admin/', admin.site.urls),

    # Прямое указание маршрутов для регистрации, логина и логаута
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),

    # Маршрут для списка самолетов
    path('aircrafts/', views.aircraft_list, name='aircrafts'),

    # Корневой маршрут, который перенаправляет на 'aircrafts'
    path('', lambda request: redirect('aircrafts')),
    path('', include('tracker.urls')),
    path('register/', views.register, name='register'),

]
