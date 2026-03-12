from tkinter import *
from tkinter import messagebox
from windows.teacher_main import TeacherMainWindow


class TeacherAuthWindow:
    def __init__(self, main_app):
        self.main_app = main_app
        self.window = Tk()  # Вернуть Tk()
        self.window.title("Ввод пароля:")
        self.window.geometry(f"{main_app.weight}x{main_app.height}")

        # Сохраняем ссылку
        main_app.window = self.window

        self.create_widgets()

        self.window.mainloop()  # Вернуть mainloop()

    def create_widgets(self):
        """Создание виджетов окна авторизации"""
        self.password_entry = Entry(self.window, show="*")
        self.password_entry.pack(pady=10)

        Label(self.window, text="Введите пароль").pack()

        Button(self.window, text="Проверить", command=self.check_password).pack(pady=10)

        self.create_bottom_panel()

    def create_bottom_panel(self):
        """Создание нижней панели"""
        bottom_frame = Frame(self.window)
        bottom_frame.pack(side=BOTTOM, fill=X, pady=10)
        Button(bottom_frame, text="Выход", command=self.main_app.exit_program).pack(side=RIGHT, padx=5)
        Button(bottom_frame, text="Назад", command=self.back).pack(side=RIGHT, padx=5)

    def check_password(self):
        """Проверить пароль"""
        if self.main_app.password == self.password_entry.get():
            messagebox.showinfo("Ввод пароля", "Добро пожаловать")
            self.window.destroy()
            TeacherMainWindow(self.main_app)
        else:
            messagebox.showinfo("Ввод пароля", "Пароль введен неверно, попробуйте еще раз")

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