from tkinter import *
from tkinter.ttk import Treeview, Style, Combobox


class Table:
    """
        Класс для отображения таблицы с данными.
    """
    def __init__(self, root, data, columns):
        """
        Инициализация таблицы.

            Параметры:
                    root: Родительский виджет.
                    data: Данные для отображения в таблице.
                    columns: Названия столбцов.
        """
        self.tree = Treeview(root, columns=columns, show='headings')
        # Настройка заголовков столбцов
        style = Style()
        style.configure("Custom.Treeview.Heading", background="red", foreground="#191919",
                        font=('Arial', 10, 'bold'))

        for col in columns:
            self.tree.heading(col, text=col.replace('Source ', '').replace('Destination ', ''), anchor=W)
            self.tree.column(col, width=100, anchor=W)

        # Цвет строк таблицы
        self.tree.tag_configure('oddrow', background='#2C2C2C', foreground='#787878')
        self.tree.tag_configure('evenrow', background='#3C3C3C', foreground='#191919')
        self.tree.tag_configure('empty', background='#2C2C2C', foreground='#191919')

        if not data:
            self.tree.insert('', 'end', values=('', '', '', '', '', '', '', ''), tags=('empty',))
        else:
            for index, row in enumerate(data):
                tag = 'oddrow' if index % 2 == 0 else 'evenrow'
                self.tree.insert('', 'end', values=row, tags=(tag,))

        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(root, orient=VERTICAL, command=self.tree.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

    def destroy(self, root):
        for widget in root.winfo_children():
            widget.destroy()


class AirportView:
    """
    Класс для представления пользовательского интерфейса.

    """
    def __init__(self, root):
        """
        Инициализация интерфейса.

            Параметры:
                    root: Родительский виджет.
        """
        self.root = root
        self.root.title("Airport Finder")
        self.root.geometry('1200x1000')
        self.root.configure(bg='#212121')

        self.style = Style()
        self.style.configure("TLabel", background='#212121', foreground='gray', font=('Arial', 10))
        self.style.configure("TButton", background='black', foreground='red', font=('Arial Bold', 10))
        self.style.configure("TEntry", font=('Arial', 10), fieldbackground='#b8c8d9')
        self.style.configure("TCombobox", font=('Arial', 10), fieldbackground='#b8c8d9')

        self.main_frame = Frame(root, bg='#212121')
        self.main_frame.pack(fill=BOTH, expand=True)

        self.top_frame = Frame(self.main_frame, bg='#212121')
        self.top_frame.pack(side=TOP, fill=X, expand=False)

        self.middle_frame = Frame(self.main_frame, bg='#212121')
        self.middle_frame.pack(side=TOP, fill=X, expand=False)

        self.bottom_frame = Frame(self.main_frame, bg='#212121')
        self.bottom_frame.pack(side=TOP, fill=BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        """
        Создать  виджеты для интерфейса.
        """
        Label(self.top_frame, text="Min latitude:", bg='#212121', fg='#787878').grid(row=0, column=0, sticky=W, pady=10, padx=10)
        self.min_lat = Combobox(self.top_frame, width=30)
        self.min_lat.grid(column=1, row=0, pady=10, padx=10)

        Label(self.top_frame, text="Max latitude:", bg='#212121', fg='#787878').grid(row=0, column=2, sticky=W, pady=10, padx=10)
        self.max_lat = Combobox(self.top_frame, width=30)
        self.max_lat.grid(column=3, row=0, pady=10, padx=10)

        Label(self.top_frame, text="Min longitude:", bg='#212121', fg='#787878').grid(row=1, column=0, sticky=W, pady=10, padx=10)
        self.min_lon = Combobox(self.top_frame, width=30)
        self.min_lon.grid(column=1, row=1, pady=10, padx=10)

        Label(self.top_frame, text="Max longitude:", bg='#212121', fg='#787878').grid(row=1, column=2, sticky=W, pady=10, padx=10)
        self.max_lon = Combobox(self.top_frame, width=30)
        self.max_lon.grid(column=3, row=1, pady=10, padx=10)

        self.btn_filter = Button(self.top_frame, text="Apply filter", command=self.on_filter_click, bg='#708090',
                                 fg='#191919')
        self.btn_filter.grid(column=2, row=2, pady=10, padx=10)

        # Создание виджетов для поиска по городу
        Label(self.middle_frame, text="City:", bg='#212121', fg='#787878').grid(row=0, column=0, sticky=W, pady=10, padx=10)
        self.city = Entry(self.middle_frame, width=30)
        self.city.grid(column=1, row=0, pady=10, padx=10)

        self.btn_search_city = Button(self.middle_frame, text="Search by City", command=self.on_city_search_click,
                                      bg='#708090', fg='#191919')
        self.btn_search_city.grid(column=2, row=0, pady=10, padx=10)

        # Создание виджетов для поиска по стране
        Label(self.middle_frame, text="Country:", bg='#212121', fg='#787878').grid(row=0, column=3, sticky=W, pady=10, padx=10)
        self.country = Entry(self.middle_frame, width=30)
        self.country.grid(column=4, row=0, pady=10, padx=10)

        self.btn_search_country = Button(self.middle_frame, text="Search by Country",
                                         command=self.on_country_search_click, bg='#708090', fg='#191919')
        self.btn_search_country.grid(column=5, row=0, pady=10, padx=10)

        # Создание виджетов для поиска по аэропорту
        Label(self.middle_frame, text="Airport:", bg='#212121', fg='#787878').grid(row=1, column=0, sticky=W, pady=10, padx=10)
        self.airport = Entry(self.middle_frame, width=30)
        self.airport.grid(column=1, row=1, pady=10, padx=10)

        self.btn_search_airport = Button(self.middle_frame, text="Search by Airport",
                                         command=self.on_airport_search_click, bg='#708090', fg='#191919')
        self.btn_search_airport.grid(column=2, row=1, pady=10, padx=10)

        # Создание виджетов для поиска по авиалиниям
        Label(self.middle_frame, text="Airline:", bg='#212121', fg='#787878').grid(row=1, column=3, sticky=W, pady=10, padx=10)
        self.airline = Entry(self.middle_frame, width=30)
        self.airline.grid(column=4, row=1, pady=10, padx=10)

        self.btn_search_airline = Button(self.middle_frame, text="Search by Airline",
                                         command=self.on_airline_search_click, bg='#708090', fg='#191919')
        self.btn_search_airline.grid(column=5, row=1, pady=10, padx=10)

        # Создание виджетов для поиска рейсов между городами
        Label(self.middle_frame, text="City 1:", bg='#212121', fg='#787878').grid(row=2, column=0, sticky=W, pady=10, padx=10)
        self.city1 = Entry(self.middle_frame, width=30)
        self.city1.grid(column=1, row=2, pady=10, padx=10)

        Label(self.middle_frame, text="City 2:", bg='#212121', fg='#787878').grid(row=3, column=0, sticky=W, pady=10, padx=10)
        self.city2 = Entry(self.middle_frame, width=30)
        self.city2.grid(column=1, row=3, pady=10, padx=10)

        self.btn_search_flights = Button(self.middle_frame, text="Search Flights", command=self.on_flight_search_click,
                                         bg='#708090', fg='#191919')
        self.btn_search_flights.grid(column=2, row=3, pady=10, padx=10)

    def set_filter_command(self, command):
        """
        Установить  команду для кнопки фильтрации.

        """
        self.btn_filter.config(command=command)

    def set_city_search_command(self, command):
        """
        Установить  команду для кнопки поиска по городу.

        """
        self.btn_search_city.config(command=command)

    def set_country_search_command(self, command):
        """
        Установить  команду для кнопки поиска по стране.

        """
        self.btn_search_country.config(command=command)

    def set_airport_search_command(self, command):
        """
        Установить  команду для кнопки поиска по аэропорту.

        """
        self.btn_search_airport.config(command=command)

    def set_airline_search_command(self, command):
        """
        Установить  команду для кнопки поиска по авиалиниям.

        """
        self.btn_search_airline.config(command=command)

    def set_flight_search_command(self, command):
        """
        Установить  команду для кнопки поиска рейсов.

        """
        self.btn_search_flights.config(command=command)

    def populate_coordinates(self, latitudes, longitudes):
        """
        Заполнить  выпадающие списки координат.

                Параметры:
                    latitudes: Список широт.
                    longitudes: Список долгот.
        """
        formatted_latitudes = [f"{lat:.1f}" for lat in latitudes]
        formatted_longitudes = [f"{lon:.1f}" for lon in longitudes]

        self.min_lat['values'] = formatted_latitudes
        self.max_lat['values'] = formatted_latitudes
        self.min_lon['values'] = formatted_longitudes
        self.max_lon['values'] = formatted_longitudes

    def get_coordinates(self):
        """
        Получить значения координат из полей ввода.

                Возвращает:
                    Кортеж из минимальной и максимальной широты и долготы.
        """
        try:
            min_lat = float(self.min_lat.get())
            max_lat = float(self.max_lat.get())
            min_lon = float(self.min_lon.get())
            max_lon = float(self.max_lon.get())

            # Проверка диапазона значений
            if not (-90 <= min_lat <= 90) or not (-90 <= max_lat <= 90):
                raise ValueError ("Широта должна быть в пределах от -90 до 90 градусов!")
            if not (-180 <= min_lon <= 180) or not  (-180 <= max_lon <= 180):
                raise  ValueError ("Долгота должна быть в пределах от -180 до 180 градусов!")

            # Проверка корректности минимальных и максимальных значений
            if min_lat > max_lat:
                raise ValueError ("Минимальная широта не может быть больше максимальной широты.")
            if min_lon > max_lon:
                raise ValueError("Минимальная долгота не может быть больше максимальной долготы.")

            return min_lat, max_lat, min_lon, max_lon
        except ValueError as e:
            self.show_error_message(f"Не верный ввод {e}!!!")
            return None, None, None, None

    def get_city(self):
        """
        Получить значение города из поля ввода.

                Возвращает:
                    Строка с названием города.
        """
        return self.city.get()

    def get_country(self):
        """
        Получить значение страны из поля ввода.

               Возвращает:
                   Строка с названием страны.
        """
        return self.country.get()

    def get_airport(self):
        """
        Получить значение аэропорта из поля ввода.

                Возвращает:
                    Строка с названием аэропорта.
        """
        return self.airport.get()

    def get_airline(self):
        """
        Получить  значение авиалинии из поля ввода.

                Возвращает:
                    Строка с названием авиалинии.
                """
        return self.airline.get()

    def get_cities(self):
        """
        Получить значения городов из полей ввода.

                Возвращает:
                    Кортеж из двух строк с названиями городов.
        """
        return self.city1.get(), self.city2.get()

    def display_airports(self, data):
        """
        Отобразить данные об аэропортах в таблице.

               Параметры:
                   data: Данные для отображения.
        """
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()
        Table(self.bottom_frame, data,
              ['Airport', 'City', 'Country', 'Latitude', 'Longitude', 'IATA', 'ICAO', 'Elevation', 'Region'])

    def display_airlines(self, data):
        """
        Отобразить данные об авиалиниях в таблице.

               Параметры:
                   data: Данные для отображения.
        """
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()
        Table(self.bottom_frame, data, ['Name', 'ICAO', 'Callsign', 'Active', 'Country'])

    def display_flights(self, data):
        """
        Отобразить данные о рейсах в таблице.

                Параметры:
                    data: Данные для отображения.
        """
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()
        Table(self.bottom_frame, data,
              ['Airline', 'Airport', 'City', 'Country', 'Airport Name', 'Destination Airport', 'Destination City', 'Destination Country', 'Destination Airport Name'])

    def show_error_message(self, message):
        """
        Показать сообщение об ошибке в новом окне.

                Параметры:
                    message: Сообщение об ошибке.
        """
        error_window = Toplevel(self.root)
        error_window.title("Error")
        error_window.configure(bg='#787878')
        Label(error_window, text=message, bg='#787878').pack(pady=10, padx=10)
        Button(error_window, text="OK", fg='#787878',  bg='red', command=error_window.destroy).pack(pady=5)

    def on_filter_click(self):
        """
        Обработчик события для кнопки фильтрации.

        """
        pass

    def on_city_search_click(self):
        """
        Обработчик события для кнопки поиска по городу.

        """
        pass

    def on_country_search_click(self):
        """
        Обработчик события для кнопки поиска по стране.

        """
        pass

    def on_airport_search_click(self):
        """
        Обработчик события для кнопки поиска по аэропорту.

        """
        pass

    def on_airline_search_click(self):
        """
        Обработчик события для кнопки поиска по авиалиниям.

        """
        pass

    def on_flight_search_click(self):
        """
        Обработчик события для кнопки поиска рейсов.
        """
        pass
