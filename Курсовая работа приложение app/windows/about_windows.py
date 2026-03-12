from tkinter import *
import os
import sys
from PIL import Image, ImageTk


class AboutWindows:
    @staticmethod
    def show_about_program(main_app):
        """Показать окно 'О программе'"""
        window = Tk()  # Вернуть Tk()
        window.title("О программе")
        window.geometry(f"{main_app.weight}x{main_app.height}")

        main_frame = Frame(window)
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        title_label = Label(main_frame, text="Электронный журнал", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))

        content_frame = Frame(main_frame)
        content_frame.pack(fill=BOTH, expand=True)

        AboutWindows.create_left_panel(content_frame, window)
        AboutWindows.create_right_panel(content_frame)

        AboutWindows.create_bottom_panel(window, main_app)

        window.mainloop()

    @staticmethod
    def show_about_autor(main_app):
        """Показать окно 'Об авторе'"""
        window = Tk()  # Вернуть Tk()
        window.title("Об авторе")
        window.geometry(f"{main_app.weight}x{main_app.height}")

        main_frame = Frame(window)
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        title_label = Label(main_frame, text="Об авторе", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 30))

        content_frame = Frame(main_frame)
        content_frame.pack(fill=BOTH, expand=True)

        AboutWindows.create_photo_panel(content_frame, window, "photo_autor.png")
        AboutWindows.create_author_info(content_frame)

        AboutWindows.create_bottom_panel(window, main_app)

        window.mainloop()

    @staticmethod
    def create_left_panel(parent, window):
        """Создать левую панель с фото"""
        left_frame = Frame(parent, relief="sunken", bd=1)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

        canvas = Canvas(left_frame, highlightthickness=0)
        canvas.pack(fill=BOTH, expand=True)

        try:
            # Получаем путь к фото
            photo_path = AboutWindows._get_asset_path("photo_program.png")

            if os.path.exists(photo_path):
                original_image = Image.open(photo_path)
                print(f"[DEBUG] Загрузил фото программы: {photo_path}")
            else:
                print(f"[DEBUG] Фото не найдено: {photo_path}")
                original_image = Image.new('RGB', (400, 300), color='lightgray')
                from PIL import ImageDraw
                draw = ImageDraw.Draw(original_image)
                draw.text((100, 140), "Фото программы", fill='black')

            def update_photo_size(event=None):
                canvas_width = canvas.winfo_width()
                canvas_height = canvas.winfo_height()

                if canvas_width <= 1 or canvas_height <= 1:
                    return

                resized_image = original_image.resize((canvas_width, canvas_height),
                                                      Image.Resampling.LANCZOS)
                photo_image = ImageTk.PhotoImage(resized_image)
                window.current_photo = photo_image

                canvas.delete("all")
                canvas.create_image(canvas_width // 2, canvas_height // 2,
                                    image=window.current_photo, anchor="center")

            canvas.bind('<Configure>', update_photo_size)
            window.after(100, update_photo_size)

        except Exception as e:
            print(f"Ошибка загрузки фото: {e}")
            import traceback
            traceback.print_exc()
            error_label = Label(left_frame, text="Фото не загружено\n\nПроверьте файл\nphoto_program.png",
                                bg="lightgray", fg="red", font=("Arial", 10), justify=CENTER)
            error_label.pack(expand=True)

    @staticmethod
    def create_right_panel(parent):
        """Создать правую панель с информацией"""
        right_frame = Frame(parent)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))

        features_title = Label(right_frame, text="Программа позволяет:",
                               font=("Arial", 14, "bold"), justify=LEFT)
        features_title.pack(anchor="w", pady=(0, 15))

        features_list = [
            "• Создавать расписания предметов",
            "• Редактировать существующие расписания",
            "• Добавлять и удалять студентов",
            "• Отмечать посещаемость занятий",
            "• Выставлять оценки за занятия",
            "• Записывать экзаменационные оценки",
            "• Просматривать успеваемость студентов",
            "• Управлять несколькими предметами",
            "• Хранить данные в базе данных SQLite",
            "• Автоматически сохранять изменения"
        ]

        for feature in features_list:
            feature_label = Label(right_frame, text=feature, font=("Arial", 12),
                                  justify=LEFT, anchor="w")
            feature_label.pack(anchor="w", pady=3)

    @staticmethod
    def create_photo_panel(parent, window, image_filename):
        """Создать панель с фотографией"""
        photo_frame = Frame(parent, bg="lightgray")
        photo_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 20))

        canvas = Canvas(photo_frame, bg="lightgray", highlightthickness=0)
        canvas.pack(fill=BOTH, expand=True)

        try:
            # Получаем путь к фото
            photo_path = AboutWindows._get_asset_path(image_filename)

            if os.path.exists(photo_path):
                original_image = Image.open(photo_path)
                print(f"[DEBUG] Загрузил фото автора: {photo_path}")
            else:
                print(f"[DEBUG] Фото не найдено: {photo_path}")
                original_image = Image.new('RGB', (400, 300), color='lightgray')
                from PIL import ImageDraw
                draw = ImageDraw.Draw(original_image)
                draw.text((100, 140), "Фото автора", fill='black')

            def update_photo_size(event=None):
                canvas_width = canvas.winfo_width()
                canvas_height = canvas.winfo_height()

                if canvas_width <= 1 or canvas_height <= 1:
                    return

                resized_image = original_image.resize((canvas_width, canvas_height),
                                                      Image.Resampling.LANCZOS)
                photo_image = ImageTk.PhotoImage(resized_image)
                window.current_photo = photo_image

                canvas.delete("all")
                canvas.create_image(canvas_width // 2, canvas_height // 2,
                                    image=window.current_photo, anchor="center")

            canvas.bind('<Configure>', update_photo_size)
            window.after(100, update_photo_size)

        except Exception as e:
            print(f"Ошибка загрузки фото: {e}")
            import traceback
            traceback.print_exc()
            error_label = Label(photo_frame, text=f"Фото не загружено\n\nПроверьте файл\n{image_filename}",
                                bg="lightgray", fg="red", font=("Arial", 10), justify=CENTER)
            error_label.pack(expand=True)

    @staticmethod
    def _get_asset_path(filename):
        """Получить путь к файлу ресурса"""
        if getattr(sys, 'frozen', False):
            # В собранном приложении
            base_path = sys._MEIPASS
            return os.path.join(base_path, 'assets', filename)
        else:
            # При разработке
            return os.path.join('assets', filename)

    @staticmethod
    def create_author_info(parent):
        """Создать панель с информацией об авторе"""
        info_frame = Frame(parent)
        info_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        author_info = [
            ("Автор:", "Arial", 14, "bold"),
            ("Студент группы 10701224", "Arial", 12),
            ("Третяк Тимофей Олегович", "Arial", 12),
            ("timatretiak@gmail.com", "Arial", 12)
        ]

        for text, font_family, size, *weight in author_info:
            font_weight = weight[0] if weight else "normal"
            info_label = Label(info_frame, text=text, font=(font_family, size, font_weight),
                               justify=LEFT, anchor="w")
            info_label.pack(anchor="w", pady=8)

    @staticmethod
    def create_bottom_panel(window, main_app):
        """Создать нижнюю панель с кнопками"""
        bottom_frame = Frame(window)
        bottom_frame.pack(side=BOTTOM, fill=X, pady=10)
        Button(bottom_frame, text="Выход", command=main_app.exit_program).pack(side=RIGHT, padx=5)
        Button(bottom_frame, text="Назад", command=lambda: AboutWindows.back_to_role(window, main_app)).pack(side=RIGHT,
                                                                                                             padx=5)

        version_frame = Frame(window)
        version_frame.pack(side=BOTTOM, fill=X, pady=5)
        version_label = Label(version_frame, text="Версия 1.0 © 2025", font=("Arial", 10), fg="gray")
        version_label.pack()

    @staticmethod
    def back_to_role(window, main_app):
        """Вернуться к окну выбора роли"""
        try:
            window.destroy()
        except:
            pass

        from windows.role_window import RoleWindow
        RoleWindow(main_app)