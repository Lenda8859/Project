class Personazh:
    def __init__(self, name, zdorove, ur_ataka):
        self.name = name
        self.zdorove = zdorove
        self.ur_ataka = ur_ataka

    def atokovat(self, drugoy_personazh):
        drugoy_personazh.zdorove -= self.ur_ataka
        print(f"{self.name} атакует {drugoy_personazh.name} и наносит {self.ur_ataka} урона!")

    def lechitsya(self, ochki_zdorovya):
        self.zdorove += ochki_zdorovya
        print(f"{self.name} восстанавливает {ochki_zdorovya} здоровье. Текущее здоровье: {self.zdorove}")

    def usilit_ataku(self, ochki_ataki):
        self.ur_ataka += ochki_ataki
        print(f"{self.name} увеличивает уровень атаки на {ochki_ataki}. Текущий уровень атаки: {self.ur_ataka}")

    def zhiv(self):
        return self.zdorove > 0

    def __str__(self):
        return f"{self.name}: Здоровье = {self.zdorove}, Уровень атаки = {self.ur_ataka}"

    def __repr__(self):
        return f"('{self.name}', {self.zdorove}, {self.ur_ataka})"

if __name__ == '__main__':
    total_test = 0
    passed_test = 0
    fail_test = 0

    def test_assert(condition, message):
        global total_test, passed_test, fail_test
        total_test += 1
        if condition:
            passed_test +=1
        else:
            fail_test +=1
            print(f"Тест не пройден {message}")




    rycar = Personazh("Рыцарь", 100, 20)
    mag = Personazh("Маг", 50, 40)
    vedma = Personazh("Ведьма", 60, 30)


#Атака

    rycar.atokovat(mag)             # Рыцарь атакует Мага и наносит 20 урона!
    test_assert(mag.zdorove == 30, "Здоровье мага должно быть 30 после атаки" )

# #Лечение

    mag.lechitsya(20) # Маг восстанавливает 20 здоровья.
    test_assert(mag.zdorove == 50, "Здоровье мага должно быть 50 после атаки")

# Усиление атаки

    rycar.usilit_ataku(10)  # Рыцарь увеличивает уровень атаки на 10.
    test_assert(rycar.ur_ataka == 30, "Уровень атаки рыцаря должен быть 30 после усиления")

# Проверка, жив ли персонаж

    test_assert(rycar.zhiv() == True, "Рыцарь должен быть жив")
    rycar.zdorove = 0
    test_assert(rycar.zhiv() == False, "Рыцарь не должен быть жив, если здоровье равно 0")

# Тестирование методов __str__ и __repr__
    print(str(vedma))
    test_assert(str(vedma) == "Ведьма: Здоровье = 60, Уровень атаки = 30", "__str__ метода должен быть правильным")
    print(repr(vedma))  # добавим печать для проверки
    test_assert(repr(vedma) == "('Ведьма', 60, 30)", "__repr__ метода должен быть правильным")

#
#  Сравнение объектов
    test_assert(rycar != vedma, "Рыцарь и Ведьма не должны быть равны")

#Резултат тестов
    print(f"Всего тестов: {total_test}")
    print(f"Пройдено тестов: {passed_test}")
    print(f"Не пройдено тестов: {fail_test}")