from tkinter import *
from tkinter import messagebox
from windows.schedule_windows import ScheduleWindows


class StudentWindow:
    def __init__(self, main_app):
        self.main_app = main_app
        self.window = Tk()  # Вернуть Tk()
        self.window.title("Режим студента")
        self.window.geometry(f"{main_app.weight}x{main_app.height}")

        # Сохраняем ссылку
        main_app.window = self.window

        self.create_widgets()

        self.window.mainloop()

    def create_widgets(self):
        """Создание виджетов окна студента"""
        Label(self.window, text="Для просмотра расписания введите свое имя и уникальный пароль").pack(pady=20)
        Label(self.window, text="Введите фамилию и имя").pack()

        self.name_get = Entry(self.window)
        self.name_get.pack(pady=10)

        Label(self.window, text="Введите уникальный пароль").pack()
        self.id_get = Entry(self.window)
        self.id_get.pack(pady=10)

        Button(self.window, text="Проверить", command=self.check_credentials).pack()

        self.create_bottom_panel()

    def create_bottom_panel(self):
        """Создание нижней панели"""
        bottom_frame = Frame(self.window)
        bottom_frame.pack(side=BOTTOM, fill=X, pady=10)
        Button(bottom_frame, text="Выход", command=self.main_app.exit_program).pack(side=RIGHT, padx=5)
        Button(bottom_frame, text="Назад", command=self.back).pack(side=RIGHT, padx=5)

    def check_credentials(self):
        """Проверить учетные данные студента"""
        student_name = self.name_get.get()
        student_id = self.id_get.get()

        if not student_name and not student_id:
            messagebox.showinfo("Внимание", "Вы не ввели свои данные")
            return
        elif not student_id:
            messagebox.showinfo("Внимание", "Вы не ввели свой пароль")
            return
        elif not student_name:
            messagebox.showinfo("Внимание", "Вы не ввели свое имя")
            return
        else:
            try:
                self.main_app.cursor.execute('''
                    SELECT id FROM global_students
                    WHERE id = ? AND student_name = ?
                ''', (student_id, student_name))

                if self.main_app.cursor.fetchone() is None:
                    messagebox.showinfo("Ошибка", "Неверная комбинация имени и ID")
                    return
            except Exception as e:
                print(f"Ошибка при проверке ID: {e}")
                messagebox.showerror("Ошибка", "Произошла ошибка при проверке данных")
                return

            messagebox.showinfo("Добро пожаловать", "Добро пожаловать")

            # Сохраняем данные студента в main_app
            self.main_app.vis_ch = True
            self.main_app.student_id = student_id  # сохраняем ID как строку
            self.main_app.student_name = student_name  # сохраняем имя

            # Закрываем текущее окно
            self.window.destroy()

            # Открываем окно просмотра расписания
            ScheduleWindows.show_edit_schedule(self.main_app)

    def back(self):
        """Вернуться назад"""
        main_app = self.main_app
        try:
            if hasattr(self, 'window') and self.window:
                self.window.destroy()
        except:
            pass

        from windows.role_window import RoleWindow
        RoleWindow(main_app)