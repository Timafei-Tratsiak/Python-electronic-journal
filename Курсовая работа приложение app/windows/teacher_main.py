from tkinter import *
from windows.schedule_windows import ScheduleWindows


class TeacherMainWindow:
    def __init__(self, main_app):
        self.main_app = main_app
        self.window = Tk()  # Вернуть Tk()
        self.window.title("Страница преподавателя")
        self.window.geometry(f"{main_app.weight}x{main_app.height}")

        # Сохраняем ссылку
        main_app.window = self.window

        self.create_widgets()

        self.window.mainloop()  # Вернуть mainloop()

    def on_closing(self):
        """Обработчик закрытия окна"""
        self.window.destroy()
        if hasattr(self.main_app, 'window4') and self.main_app.window4 == self.window:
            self.main_app.window4 = None

    def create_widgets(self):
        """Создание виджетов главного окна преподавателя"""
        Label(self.window,
              text="Добро пожаловать, преподаватель! \n"
                   "Здесь вы можете создавать, удалять и редактировать расписание предмета,\n"
                   "а также выставлять оценки ученикам").pack(pady=10)

        button_frame = Frame(self.window)
        button_frame.pack(pady=10)

        Button(button_frame, text="Создать расписание предмета",
               command=self.create_schedule).pack(pady=5)
        Button(button_frame, text="Редактировать расписание",
               command=self.edit_schedule).pack(pady=5)
        Button(button_frame, text="Выставить оценку",
               command=self.rate_students).pack(pady=5)

        self.create_bottom_panel()

    def create_bottom_panel(self):
        """Создание нижней панели"""
        bottom_frame = Frame(self.window)
        bottom_frame.pack(side=BOTTOM, fill=X, pady=10)
        Button(bottom_frame, text="Выход", command=self.main_app.exit_program).pack(side=RIGHT, padx=5)
        Button(bottom_frame, text="Назад", command=self.back).pack(side=RIGHT, padx=5)

    def create_schedule(self):
        """Создать расписание"""
        self.window.destroy()
        ScheduleWindows.show_create_schedule(self.main_app)

    def edit_schedule(self):
        """Редактировать расписание"""
        self.main_app.vis_ch = False
        self.main_app.sche_r = False
        self.window.destroy()
        ScheduleWindows.show_edit_schedule(self.main_app)

    def rate_students(self):
        """Выставить оценки"""
        self.main_app.sche_r = True
        self.main_app.vis_ch = False
        self.window.destroy()
        ScheduleWindows.show_rate_schedule(self.main_app)

    def back(self):
        """Вернуться назад"""
        main_app = self.main_app
        try:
            if hasattr(self, 'window') and self.window:
                self.window.destroy()
        except:
            pass

        from windows.teacher_auth import TeacherAuthWindow
        TeacherAuthWindow(main_app)