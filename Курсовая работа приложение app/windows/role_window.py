from tkinter import *
from tkinter import messagebox
from windows.teacher_auth import TeacherAuthWindow
from windows.student_window import StudentWindow
from windows.about_windows import AboutWindows


class RoleWindow:
    def __init__(self, main_app):
        self.main_app = main_app
        self.window = Tk()
        self.window.title("Выбор роли:")
        self.window.geometry(f"{main_app.weight}x{main_app.height}")

        # УНИЧТОЖАЕМ предыдущее главное окно
        if hasattr(main_app, 'window') and main_app.window:
            try:
                main_app.window.destroy()
            except:
                pass

        # Сохраняем ссылку на новое окно
        main_app.window = self.window

        self.create_menu()
        self.create_widgets()

        self.window.mainloop()

    def create_menu(self):
        """Создание меню"""
        # Удаляем старое меню если есть
        try:
            if hasattr(self.window, 'menu') and self.window.menu:
                self.window.config(menu=None)
        except:
            pass

        menubar = Menu(self.window)

        information_menu = Menu(menubar, tearoff=0)
        information_menu.add_command(label="О программе", command=self.about_program)
        information_menu.add_command(label="Об авторе", command=self.about_autor)
        menubar.add_cascade(label="Information", menu=information_menu)

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="Как пользоваться программой",
                              command=self.main_app.help_instruction)
        menubar.add_cascade(label="Help", menu=help_menu)

        exit_menu = Menu(menubar, tearoff=0)
        exit_menu.add_command(label="Выход", command=self.main_app.exit_program)
        menubar.add_cascade(label="Exit", menu=exit_menu)

        self.window.config(menu=menubar)
        # Сохраняем ссылку на меню
        self.window.menu = menubar

    def create_widgets(self):
        """Создание виджетов окна"""
        Label(self.window, text="Выберите, кем вы являетесь").pack(pady=40)

        role_frame = Frame(self.window)
        role_frame.pack(pady=20)

        Button(role_frame, text="Преподаватель",
               command=self.open_teacher_window).pack(side=RIGHT, padx=40)
        Button(role_frame, text="Студент",
               command=self.open_student_window).pack(side=LEFT, padx=40)

        self.create_bottom_panel()

    def create_bottom_panel(self):
        """Создание нижней панели"""
        bottom_frame = Frame(self.window)
        bottom_frame.pack(side=BOTTOM, fill=X, pady=10)
        Button(bottom_frame, text="О программе", command=self.about_program).pack(side=LEFT, padx=5)
        Button(bottom_frame, text="Об авторе", command=self.about_autor).pack(side=LEFT, padx=5)
        Button(bottom_frame, text="Выход", command=self.main_app.exit_program).pack(side=RIGHT, padx=5)

    def about_program(self):
        """Открыть окно 'О программе'"""
        # Используем after для отложенного выполнения
        self.window.after(10, self._open_about_program)

    def _open_about_program(self):
        """Внутренний метод для открытия 'О программе'"""
        main_app = self.main_app

        try:
            self.window.destroy()
        except:
            pass

        AboutWindows.show_about_program(main_app)

    def about_autor(self):
        """Открыть окно 'Об авторе'"""
        # Используем after для отложенного выполнения
        self.window.after(10, self._open_about_autor)

    def _open_about_autor(self):
        """Внутренний метод для открытия 'Об авторе'"""
        main_app = self.main_app

        try:
            self.window.destroy()
        except:
            pass

        AboutWindows.show_about_autor(main_app)

    def open_teacher_window(self):
        """Открыть окно авторизации преподавателя"""
        # Используем after для отложенного выполнения
        self.window.after(10, self._open_teacher_window)

    def _open_teacher_window(self):
        """Внутренний метод для открытия окна преподавателя"""
        main_app = self.main_app

        try:
            self.window.destroy()
        except:
            pass

        from windows.teacher_auth import TeacherAuthWindow
        TeacherAuthWindow(main_app)

    def open_student_window(self):
        """Открыть окно студента"""
        # Используем after для отложенного выполнения
        self.window.after(10, self._open_student_window)

    def _open_student_window(self):
        """Внутренний метод для открытия окна студента"""
        main_app = self.main_app

        try:
            self.window.destroy()
        except:
            pass

        from windows.student_window import StudentWindow
        StudentWindow(main_app)

    def close_window(self):
        """Безопасное закрытие окна"""
        try:
            if hasattr(self, 'window') and self.window:
                self.window.destroy()
        except:
            pass

    def __del__(self):
        """Деструктор для очистки"""
        try:
            if hasattr(self, 'window') and self.window:
                self.window.destroy()
        except:
            pass