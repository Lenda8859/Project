class Personazh:
    def __init__(self, imya, zdorove, ur_ataka):
        self.imya = imya
        self.zdorove = zdorove
        self.ur_ataka = ur_ataka

    def atakovat(self, drugoy_personazh):
        drugoy_personazh.zdorove -= self.ur_ataka
        print(f"{self.imya} атакует {drugoy_personazh.imya} и наносит {self.ur_ataka} урона!")

    def lechitsya(self, ochki_zdorovya):
        self.zdorove += ochki_zdorovya
        print(f"{self.imya} восстанавливает {ochki_zdorovya} здоровья. Текущее здоровье: {self.zdorove}")

    def usilit_ataku(self, ochki_ataki):
        self.ur_ataka += ochki_ataki
        print(f"{self.imya} увеличивает уровень атаки на {ochki_ataki}. Текущий уровень атаки: {self.ur_ataka}")

    def zhiv(self):
        return self.zdorove > 0

    def __str__(self):
        return f"{self.imya}: Здоровье = {self.zdorove}, Уровень атаки = {self.ur_ataka}"

    def __repr__(self):
        return f"Personazh('{self.imya}', {self.zdorove}, {self.ur_ataka})"

if __name__ == '__main__':
    total_tests = 0
    passed_tests = 0
    failed_tests = 0

    def test_assert(condition, message):
        global total_tests, passed_tests, failed_tests
        total_tests += 1
        if condition:
            passed_tests += 1
        else:
            failed_tests += 1
            print(f"Тест не пройден: {message}")

    # Тесты
    rycar = Personazh("Рыцарь", 100, 20)
    mag = Personazh("Маг", 50, 40)
    vedma = Personazh("Ведьма", 60, 30)

    # Тест атаки
    rycar.atakovat(mag)
    test_assert(mag.zdorove == 30, "Здоровье мага должно быть 30 после атаки")

    # Тест лечения
    mag.lechitsya(20)
    test_assert(mag.zdorove == 50, "Здоровье мага должно быть 50 после лечения")

    # Тест усиления атаки
    rycar.usilit_ataku(10)
    test_assert(rycar.ur_ataka == 30, "Уровень атаки рыцаря должен быть 30 после усиления")

    # Тест жив/не жив
    test_assert(rycar.zhiv() == True, "Рыцарь должен быть жив")
    rycar.zdorove = 0
    test_assert(rycar.zhiv() == False, "Рыцарь не должен быть жив, если здоровье равно 0")

    # Тест __str__ и __repr__
    test_assert(str(vedma) == "Ведьма: Здоровье = 60, Уровень атаки = 30", "__str__ метода должен быть правильным")
    print(repr(vedma)) # добавим печать для проверки
    test_assert(repr(vedma) == "Personazh('Ведьма', 60, 30)", "__repr__ метода должен быть правильным")

    # Сравнение объектов
    test_assert(rycar != vedma, "Рыцарь и Ведьма не должны быть равны")

    # Результаты тестов
    print(f"Всего тестов: {total_tests}")
    print(f"Пройдено тестов: {passed_tests}")
    print(f"Не пройдено тестов: {failed_tests}")


