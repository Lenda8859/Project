from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .forms import RegisterForm, FilterForm, AircraftFilterForm
from cachetools import TTLCache
import requests
from datetime import datetime
from django.http import HttpResponseBadRequest
from .utils import get_flight_trajectory
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import FavoriteAircraft


def register(request):
    """ Представление для регистрации новых пользователей """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Вход под новым пользователем
            return redirect('aircrafts')  # Перенаправляем на страницу с самолетами
    else:
        form = RegisterForm()
    return render(request, 'tracker/register.html', {'form': form})


def user_login(request):
    """ Представление для входа пользователей """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('aircrafts')  # Перенаправляем на страницу с самолетами
    else:
        form = AuthenticationForm()
    return render(request, 'tracker/login.html', {'form': form})

def custom_logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # Перенаправляем на страницу входа после выхода
    return render(request, 'tracker/logout.html')  # Отображаем форму с кнопкой "Выход"


@login_required
def aircraft_list(request):
    """ Список самолетов с фильтрацией по параметрам """
    # Получаем данные с OpenSky API
    aircrafts = get_aircraft_data()

    # Получаем список избранных самолётов для текущего пользователя
    favorite_aircraft_ids = FavoriteAircraft.objects.filter(user=request.user).values_list('aircraft_id', flat=True)

    # Проверка и замена None на значения по умолчанию
    for ac in aircrafts:
        if ac[6] is None:
            ac[6] = 37.7749  # Широта по умолчанию (Сан-Франциско)
        if ac[5] is None:
            ac[5] = -122.4194  # Долгота по умолчанию (Сан-Франциско)

    # Применение фильтров
    form = AircraftFilterForm(request.GET)
    if form.is_valid():
        icao24 = form.cleaned_data.get('icao24')
        country = form.cleaned_data.get('country')
        min_latitude = form.cleaned_data.get('min_latitude')
        max_latitude = form.cleaned_data.get('max_latitude')
        min_longitude = form.cleaned_data.get('min_longitude')
        max_longitude = form.cleaned_data.get('max_longitude')

        # Фильтрация по ICAO24 (ID воздушного судна)
        if icao24:
            aircrafts = [ac for ac in aircrafts if ac[0].lower() == icao24.lower()]

        # Фильтрация по стране
        if country:
            aircrafts = [ac for ac in aircrafts if ac[2] == country]

        # Фильтрация по широте и долготе
        if min_latitude is not None:
            aircrafts = [ac for ac in aircrafts if ac[6] is not None and float(ac[6]) >= min_latitude]
        if max_latitude is not None:
            aircrafts = [ac for ac in aircrafts if ac[6] is not None and float(ac[6]) <= max_latitude]
        if min_longitude is not None:
            aircrafts = [ac for ac in aircrafts if ac[5] is not None and float(ac[5]) >= min_longitude]
        if max_longitude is not None:
            aircrafts = [ac for ac in aircrafts if ac[5] is not None and float(ac[5]) <= max_longitude]

    # Передаём данные в шаблон
    return render(request, 'tracker/aircraft_list.html', {
        'aircrafts': aircrafts,
        'form': form,
        'favorite_aircraft_ids': favorite_aircraft_ids  # Передаём избранные самолёты
    })


@login_required
def toggle_favorite(request, aircraft_id):
    """ Добавление/удаление самолёта из избранного """
    # Получаем данные о самолёте из POST-запроса
    aircraft_data = request.POST.get('aircraft_data')

    if not aircraft_data:
        # Если данные отсутствуют, выводим сообщение об ошибке и перенаправляем обратно
        messages.error(request, 'Данные о самолёте отсутствуют.')
        return redirect('aircrafts')

    # Разделяем полученные данные на страну, широту и долготу
    aircraft_info = aircraft_data.split(',')
    if len(aircraft_info) < 3:
        # Проверяем, что данные полны и корректны
        messages.error(request, 'Некорректные данные о самолёте.')
        return redirect('aircrafts')

    # Получаем страну, широту и долготу
    country = aircraft_info[0]
    latitude = aircraft_info[1]
    longitude = aircraft_info[2]

    # Проверяем наличие самолёта в избранном и добавляем или удаляем его
    favorite, created = FavoriteAircraft.objects.get_or_create(
        user=request.user,
        aircraft_id=aircraft_id,
        defaults={'country': country, 'latitude': latitude, 'longitude': longitude}
    )

    if not created:
        # Если самолёт уже был в избранном, удаляем его
        favorite.delete()
        messages.info(request, f'Самолёт с ID {aircraft_id} был удалён из избранного.')
    else:
        messages.success(request, f'Самолёт с ID {aircraft_id} был добавлен в избранное.')

    return redirect('aircrafts')


@login_required
def favorite_list(request):
    """Отображение списка избранных самолётов."""
    # Получаем все избранные самолёты для текущего пользователя
    favorites = FavoriteAircraft.objects.filter(user=request.user)

    # Передаём список избранных самолётов в шаблон
    return render(request, 'tracker/favorites_list.html', {'favorites': favorites})


@login_required
def flight_trajectory(request):
    """Отображение траектории полета по самолету"""
    icao24 = request.GET.get('icao24')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')


    # Проверка на наличие параметров
    if not start_time or not end_time:
        return HttpResponseBadRequest("Отсутствуют параметры start_time или end_time")

    # Преобразование времени в UNIX формат
    try:
        start_time_unix = int(datetime.strptime(start_time, '%Y-%m-%dT%H:%M').timestamp())
        end_time_unix = int(datetime.strptime(end_time, '%Y-%m-%dT%H:%M').timestamp())
    except ValueError:
        return HttpResponseBadRequest("Invalid date format")
    print(f"ICAO24: {icao24}, Start Time (UNIX): {start_time_unix}, End Time (UNIX): {end_time_unix}")

    # Вызов функции get_flight_trajectory с правильными аргументами
    flight_data = get_flight_trajectory(icao24, start_time_unix, end_time_unix)
    print(f"Данные о траектории полёта для {icao24}: {flight_data}")

    return render(request, 'tracker/flight_trajectory.html', {'flight_data': flight_data, 'icao24': icao24})


# Вспомогательные функции для работы с данными самолета
aircraft_cache = TTLCache(maxsize=1, ttl=300)

def get_aircraft_data():
    """ Получение данных о самолетах через OpenSky API """
    if 'aircrafts' in aircraft_cache:
        return aircraft_cache['aircrafts']

    url = 'https://opensky-network.org/api/states/all'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('states', [])
    elif response.status_code == 429:
        print("Error: Too Many Requests. Please wait before making more requests.")
    else:
        print(f"Error: Received status code {response.status_code}")
    return []

from .utils import get_active_aircrafts  # Импорт функции из utils.py

@login_required
def active_aircrafts_view(request):
    # Получаем активные самолёты
    active_aircrafts = get_active_aircrafts()

    # Временный вывод данных в консоль сервера
    for aircraft in active_aircrafts:
        print(f"ICAO24: {aircraft[0]}, Страна: {aircraft[2]}")

    # Передача данных в шаблон для отображения на странице
    return render(request, 'tracker/active_aircrafts.html', {'aircrafts': active_aircrafts})