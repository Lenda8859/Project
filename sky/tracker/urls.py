from django.urls import path
from . import views
from .views import toggle_favorite, favorite_list

urlpatterns = [
    # Представление для регистрации
    path('register/', views.register, name='register'),

    # Представление для логина
    path('login/', views.user_login, name='login'),

    # Представление для выхода
    path('logout/', views.custom_logout_view, name='logout'),

    # Страница со списком воздушных судов
    path('aircrafts/', views.aircraft_list, name='aircrafts'),

    # Добавление в "избранное" или удаление
    path('aircrafts/<str:aircraft_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),

    # Траектория полета
    path('trajectory/', views.flight_trajectory, name='flight_trajectory'),

    # Страница с избранными самолётами
    path('favorites/', views.favorite_list, name='favorites'),
]
