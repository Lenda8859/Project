function initAircraftMap() {
    // Центр карты по умолчанию
    var mapCenter = { lat: 37.7749, lng: -122.4194 };  // Координаты Сан-Франциско по умолчанию

    // Создание карты
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 4,
        center: mapCenter
    });

    // Перебираем все самолёты и создаём маркеры для каждого
    {% for aircraft in aircrafts %}
        var aircraftLat = parseFloat("{{ aircraft.6|default:'37.7749'|escapejs }}");
        var aircraftLng = parseFloat("{{ aircraft.5|default:'-122.4194'|escapejs }}");

        // Проверяем, что координаты валидны
        if (!isNaN(aircraftLat) && !isNaN(aircraftLng)) {
            var marker = new google.maps.Marker({
                position: { lat: aircraftLat, lng: aircraftLng },
                map: map,
                title: 'ID: {{ aircraft.0 }} ({{ aircraft.1 }})'
            });
        }
    {% endfor %}
}

// Инициализация карты при загрузке страницы
window.onload = initAircraftMap;
