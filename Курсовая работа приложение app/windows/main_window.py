from tkinter import *
from tkinter import messagebox
from database import Database
from config import Config
from windows.role_window import RoleWindow


class Window:
    def __init__(self):
        self.current_sort_mode = 'alphabetical'
        self.sort_button = None
        self.current_subject_id = None
        self.vis_ch = False
        self.sche_r = False
        self.current_window = None

        self.window = Tk()
        self.window.title("Контроль успеваемости")
        self.weight = Config.WINDOW_WIDTH
        self.height = Config.WINDOW_HEIGHT
        self.window.geometry(f"{self.weight}x{self.height}")

        self.create_widgets()
        self.init_database()
        self.setup_timer()
        self.password = Config.TEACHER_PASSWORD

        self.window.mainloop()

    def create_widgets(self):
        """Создание виджетов главного окна"""
        # Заголовки
        Label(self.window, text="Белорусский национальный технический университет",
              font=("Arial", 14)).pack(side=TOP, pady=10)
        Label(self.window, text="Факультет информационных технологий и робототехники",
              font=("Arial", 14)).pack(side=TOP)
        Label(self.window, text="Кафедра программного обеспечения информационных систем и технологий",
              font=("Arial", 14)).pack(side=TOP)
        Label(self.window, text="Курсовая работа", font=("Arial", 14, "bold")).pack(side=TOP, pady=(35, 0))
        Label(self.window, text="по дисциплине Языки программирования", font=("Arial", 14)).pack(side=TOP)
        Label(self.window, text="Контроль успеваемости студентов",
              font=("Arial", 14, "bold")).pack(side=TOP, pady=(0, 5))

        # Основной контент
        content_frame = Frame(self.window)
        content_frame.pack(fill=BOTH, expand=True)

        self.create_left_panel(content_frame)
        self.create_right_panel(content_frame)
        self.create_bottom_panel()

    def create_left_panel(self, parent):
        """Создание левой панели с фото"""
        left_frame = Frame(parent, relief="sunken", bd=1)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

        canvas = Canvas(left_frame, highlightthickness=0, bg="lightgray")
        canvas.pack(fill=BOTH, expand=True)

        try:
            from PIL import Image, ImageTk
            import os
            import sys

            print(f"[DEBUG] Загрузка фото...")
            print(f"[DEBUG] _MEIPASS: {getattr(sys, '_MEIPASS', 'НЕТ')}")
            print(f"[DEBUG] frozen: {getattr(sys, 'frozen', False)}")

            if getattr(sys, 'frozen', False):
                # В СОБРАННОМ ПРИЛОЖЕНИИ
                base_path = sys._MEIPASS
                print(f"[DEBUG] Режим: frozen app")
                print(f"[DEBUG] base_path (sys._MEIPASS): {base_path}")

                # Файлы в base_path/assets/
                photo_path = os.path.join(base_path, 'assets', 'photo_program.png')
                print(f"[DEBUG] Ищу фото по пути: {photo_path}")

            else:
                # ПРИ РАЗРАБОТКЕ
                print(f"[DEBUG] Режим: разработка")
                photo_path = 'assets/photo_program.png'

            print(f"[DEBUG] Финальный путь: {photo_path}")
            print(f"[DEBUG] Файл существует: {os.path.exists(photo_path)}")

            if os.path.exists(photo_path):
                print(f"[DEBUG] Загружаю фото...")
                self.original_image_program = Image.open(photo_path)
                print(f"[DEBUG] Фото загружено, размер: {self.original_image_program.size}")
            else:
                # Заглушка
                print(f"[DEBUG] Фото не найдено, создаю заглушку")
                self.original_image_program = Image.new('RGB', (400, 300), color='lightgray')

                # Добавим текст
                try:
                    from PIL import ImageDraw
                    draw = ImageDraw.Draw(self.original_image_program)
                    draw.text((100, 140), "Фото программы", fill='black')
                except:
                    pass

            # Остальной код без изменений
            def update_photo_size(event=None):
                canvas_width = canvas.winfo_width()
                canvas_height = canvas.winfo_height()

                if canvas_width <= 1 or canvas_height <= 1:
                    return

                resized_image = self.original_image_program.resize((canvas_width, canvas_height),
                                                                   Image.Resampling.LANCZOS)
                photo_image = ImageTk.PhotoImage(resized_image)
                self.window.current_photo = photo_image

                canvas.delete("all")
                canvas.create_image(canvas_width // 2, canvas_height // 2,
                                    image=self.window.current_photo, anchor="center")

            canvas.bind('<Configure>', update_photo_size)
            self.window.after(100, update_photo_size)

        except Exception as e:
            print(f"Ошибка загрузки фото: {e}")
            import traceback
            traceback.print_exc()
            error_label = Label(left_frame, text="Фото не загружено",
                                bg="lightgray", fg="red", font=("Arial", 10), justify=CENTER)
            error_label.pack(expand=True)

    def create_right_panel(self, parent):
        """Создание правой панели с информацией"""
        right_frame = Frame(parent)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))

        Label(right_frame, text="Выполнил: Студент группы 10701224",
              font=("Arial", 14)).pack(anchor="w", pady=(35, 5))
        Label(right_frame, text="Третяк Тимофей Олегович",
              font=("Arial", 14)).pack(anchor="w", pady=(0, 20))

        Label(right_frame, text="Преподаватель: к.ф.-м.н., доц.",
              font=("Arial", 14)).pack(anchor="w", pady=(0, 5))
        Label(right_frame, text="Сидорик Валерий Владимирович",
              font=("Arial", 14)).pack(anchor="w", pady=(0, 20))

    def create_bottom_panel(self):
        """Создание нижней панели с кнопками"""
        bottom_frame = Frame(self.window)
        bottom_frame.pack(side=BOTTOM, fill=X, pady=14)

        Label(bottom_frame, text="Минск, 2025", font=("Arial", 14)).pack(side=TOP, anchor="center")

        Button(bottom_frame, text="Выход", command=self.exit_program).pack(side=RIGHT, padx=5)
        Button(bottom_frame, text="Дальше", command=self.open_window2).pack(side=RIGHT, padx=5)

    def init_database(self):
        """Инициализация базы данных"""
        self.db = Database()
        self.conn = self.db.conn
        self.cursor = self.db.cursor

    def setup_timer(self):
        """Настройка таймера автозакрытия"""
        self.auto_close_timer = None
        self.first_window_active = True
        self.start_first_window_timer()

    def start_first_window_timer(self):
        """Запуск таймера для первого окна"""
        self.auto_close_timer = self.window.after(Config.AUTO_CLOSE_TIME, self.auto_close_program)

    def stop_first_window_timer(self):
        """Остановка таймера"""
        if self.auto_close_timer:
            self.window.after_cancel(self.auto_close_timer)
            self.auto_close_timer = None

    def auto_close_program(self):
        """Автоматическое закрытие программы"""
        if self.first_window_active:
            self.exit_program()

    def open_window2(self):
        """Открытие окна выбора роли"""
        self.stop_first_window_timer()
        self.first_window_active = False

        # НЕ уничтожаем окно сразу, пусть RoleWindow сделает это
        # Просто запускаем RoleWindow
        RoleWindow(self)

    def help_instruction(self):
        """Показать инструкцию"""
        instruction_text = """Инструкция по использованию программы "Контроль успеваемости"

Основные возможности:

Для преподавателей:
1. Создание предметов - добавление новых учебных дисциплин
2. Формирование расписания - планирование занятий и лабораторных работ
3. Управление студентами - добавление и редактирование списка студентов
4. Отметка посещаемости - ведение учета присутствия на занятиях
5. Выставление оценок - фиксация результатов выполнения работ
6. Экзаменационные оценки - внесение итоговых оценок за семестр

Для студентов:
1. Просмотр расписания - доступ к графику занятий
2. Мониторинг успеваемости - отслеживание своих оценок и посещаемости
3. Просмотр экзаменационных результатов - ознакомление с итоговыми оценками

Порядок работы:
1. Выберите вашу роль при входе в программу
2. Следуйте инструкциям в соответствующих разделах
3. Сохраняйте изменения для сохранения данных в базе
4. Используйте кнопку "Назад" для возврата к предыдущим экранам"""

        messagebox.showinfo("Как пользоваться программой", instruction_text)

    def exit_program(self):
        """Выход из программы - полное закрытие"""
        try:
            # Закрываем все окна Tkinter
            try:
                if hasattr(self, 'window') and self.window:
                    self.window.quit()
                    self.window.destroy()
            except:
                pass

            # Закрываем базу данных
            try:
                if hasattr(self, 'db'):
                    self.db.disconnect()
            except:
                pass

            # Завершаем процесс Python
            import os
            import sys
            os._exit(0)

        except Exception as e:
            print(f"Ошибка при выходе: {e}")
            import os
            os._exit(1)