from tkinter import *
from tkinter import messagebox
from config import Config
from utils.validators import validate_integer_input, validate_subject_name, validate_grade_input
from utils.sorters import sort_by_marks, sort_by_alphabet, calculate_average_grade


class ScheduleWindows:
    @staticmethod
    def show_create_schedule(main_app):
        """Показать окно создания расписания"""
        window = Tk()  # Вернуть Tk()
        main_app.window6 = window
        window.title("Создание расписания:")
        window.geometry(f"{main_app.weight}x{main_app.height}")


        # Функции для валидации
        def validate_integer_input_local(P):
            if P == "":
                return True
            if P.isdigit():
                num = int(P)
                return 1 <= num <= 100
            return False

        def validate_subject_name_local(P):
            if len(P) <= 100:
                return True
            return False

        # Регистрация функций валидации
        int_vcmd = (main_app.window6.register(validate_integer_input_local), '%P')
        name_vcmd = (main_app.window6.register(validate_subject_name_local), '%P')

        # Валидация названия предмета (уникальность)
        def validate_subject_unique():
            subject_name = main_app.object_entry.get().strip()
            if not subject_name:
                messagebox.showerror("Ошибка", "Введите название предмета")
                return False

            # Проверяем уникальность в базе данных
            main_app.cursor.execute("SELECT COUNT(*) FROM subjects WHERE name = ?", (subject_name,))
            count = main_app.cursor.fetchone()[0]

            if count > 0:
                return False
            return True

        Label(main_app.window6, text="Введите название предмета").pack()
        main_app.object_entry = Entry(main_app.window6, validate="key", validatecommand=name_vcmd)
        main_app.object_entry.pack()

        Label(main_app.window6, text="Введите количество занятий (1-100)").pack()
        main_app.lesson_entry = Entry(main_app.window6, validate="key", validatecommand=int_vcmd)
        main_app.lesson_entry.pack()

        Label(main_app.window6, text="Введите количество студентов (1-100)").pack()
        main_app.student_entry = Entry(main_app.window6, validate="key", validatecommand=int_vcmd)
        main_app.student_entry.pack()

        main_app.has_exam = False

        def toggle_exam():
            main_app.has_exam = not main_app.has_exam
            exam_checkbox.config(text="Да ✓" if main_app.has_exam else "Да")

        Label(main_app.window6, text="Есть ли экзамен по предмету").pack()
        exam_checkbox = Checkbutton(main_app.window6, text="Да", command=toggle_exam)
        exam_checkbox.pack()

        def validated_next_1():
            # Проверка всех полей
            errors = []

            # Проверка названия предмета
            subject_name = main_app.object_entry.get().strip()
            if not subject_name:
                errors.append("Введите название предмета")
            elif not validate_subject_unique():
                errors.append(f"Предмет с названием '{subject_name}' уже существует")

            # Проверка количества занятий
            lessons = main_app.lesson_entry.get().strip()
            if not lessons:
                errors.append("Введите количество занятий")
            elif not lessons.isdigit():
                errors.append("Количество занятий должно быть числом")
            elif not (1 <= int(lessons) <= 100):
                errors.append("Количество занятий должно быть от 1 до 100")

            # Проверка количества студентов
            students = main_app.student_entry.get().strip()
            if not students:
                errors.append("Введите количество студентов")
            elif not students.isdigit():
                errors.append("Количество студентов должно быть числом")
            elif not (1 <= int(students) <= 100):
                errors.append("Количество студентов должно быть от 1 до 100")

            if errors:
                messagebox.showerror("Ошибка ввода", "\n".join(errors))
                return

            ScheduleWindows.next_1(main_app)

        button_save = Button(main_app.window6, text="Создать", command=validated_next_1)
        button_save.pack()

        # Информационная метка
        info_label = Label(main_app.window6, text="* Все поля обязательны для заполнения",
                           font=("Arial", 9), fg="gray")
        info_label.pack(pady=5)

        bottom_frame = Frame(main_app.window6)
        bottom_frame.pack(side=BOTTOM, fill=X, pady=10)
        Button(bottom_frame, text="Выход", command=main_app.exit_program).pack(side=RIGHT, padx=5)
        Button(bottom_frame, text="Назад", command=lambda: ScheduleWindows.back_from_window6(main_app)).pack(side=RIGHT, padx=5)
        window.mainloop()

    @staticmethod
    def next_1(main_app):
        # Скрываем окно 6 вместо уничтожения
        main_app.window6.withdraw()

        # Создаем новое окно Tk()
        main_app.window7 = Tk()
        window = main_app.window7
        window.title("Создание расписания:")
        window.geometry("900x700")

        subject_name = main_app.object_entry.get()
        num_lessons = int(main_app.lesson_entry.get())
        num_students = int(main_app.student_entry.get())
        has_exam = main_app.has_exam

        title_label = Label(window, text=subject_name, font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        main_container = Frame(main_app.window7)
        main_container.pack(pady=10, fill=BOTH, expand=True)

        canvas = Canvas(main_container, bg='systemWindowBackgroundColor')
        v_scrollbar = Scrollbar(main_container, orient="vertical", command=canvas.yview, width=20)
        h_scrollbar = Scrollbar(main_container, orient="horizontal", command=canvas.xview, width=20)

        scrollable_frame = Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        def on_canvas_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_arrows(event):
            if event.keysym == 'Up':
                canvas.yview_scroll(-1, "units")
            elif event.keysym == 'Down':
                canvas.yview_scroll(1, "units")
            elif event.keysym == 'Left':
                canvas.xview_scroll(-1, "units")
            elif event.keysym == 'Right':
                canvas.xview_scroll(1, "units")

        def on_mouse_wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def on_shift_wheel(event):
            canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

        def set_focus(event):
            widget = event.widget
            if not isinstance(widget, (Entry, Checkbutton)):
                canvas.focus_set()

        scrollable_frame.bind("<Configure>", on_canvas_configure)
        canvas.bind("<KeyPress>", on_arrows)
        canvas.bind("<Button-1>", set_focus)
        canvas.bind("<MouseWheel>", on_mouse_wheel)
        canvas.bind("<Shift-MouseWheel>", on_shift_wheel)

        headers = ["Студенты"] + [f"Занятие {i + 1}" for i in range(num_lessons)]
        if has_exam:
            headers.append("Экзамен")

        for col, header in enumerate(headers):
            width = 20 if col == 0 else 15
            header_label = Label(scrollable_frame, text=header, relief="solid", borderwidth=1,
                                 width=width, height=2, bg="lightgray")
            header_label.grid(row=0, column=col, sticky="nsew")

        Label(scrollable_frame, text="Дата/Лаб.раб.", relief="solid", borderwidth=1,
              bg="lightblue", width=20).grid(row=1, column=0, sticky="nsew")

        main_app.date_entries = []
        main_app.lab_entries = []

        for col in range(1, num_lessons + 1):
            entry_frame = Frame(scrollable_frame, relief="solid", borderwidth=1, width=150)
            entry_frame.grid(row=1, column=col, sticky="nsew")
            entry_frame.grid_propagate(False)

            date_entry = Entry(entry_frame, width=12)
            date_entry.pack(side=TOP, fill=X, padx=2, pady=1)
            date_entry.insert(0, f"Дата {col}")

            lab_entry = Entry(entry_frame, width=12)
            lab_entry.pack(side=BOTTOM, fill=X, padx=2, pady=1)
            lab_entry.insert(0, "Лаб. №")

            main_app.date_entries.append(date_entry)
            main_app.lab_entries.append(lab_entry)

        if has_exam:
            exam_date_frame = Frame(scrollable_frame, relief="solid", borderwidth=1, width=150)
            exam_date_frame.grid(row=1, column=num_lessons + 1, sticky="nsew")
            exam_date_frame.grid_propagate(False)

            exam_date_entry = Entry(exam_date_frame, width=12)
            exam_date_entry.pack(side=TOP, fill=X, padx=2, pady=1)
            exam_date_entry.insert(0, "Дата экзамена")
            main_app.exam_date_entry = exam_date_entry

        main_app.student_name_entries = []
        main_app.attendance_vars = []
        main_app.grade_entries = []
        main_app.exam_entries = []

        def focus_name_student(event):
            system_bg = main_app.window7.cget('bg')
            for entry in main_app.student_name_entries:
                entry.configure(highlightbackground=system_bg, highlightthickness=1)
            for row in range(2, num_students + 2):
                for col in range(len(headers)):
                    cells = scrollable_frame.grid_slaves(row=row, column=col)
                    if cells:
                        cells[0].configure(highlightbackground=system_bg, highlightthickness=1)

            event.widget.configure(highlightbackground="#FFDAB9", highlightthickness=1)
            row = event.widget.grid_info()['row']
            for col in range(len(headers)):
                cells = scrollable_frame.grid_slaves(row=row, column=col)
                if cells:
                    cells[0].configure(highlightbackground="#FFDAB9", highlightthickness=1)

        def unfocus_name_student(event):
            system_bg = main_app.window7.cget('bg')
            row = event.widget.grid_info()['row']
            event.widget.configure(highlightbackground=system_bg, highlightthickness=1)
            for col in range(len(headers)):
                cells = scrollable_frame.grid_slaves(row=row, column=col)
                if cells:
                    cells[0].configure(highlightbackground=system_bg, highlightthickness=1)

        for row in range(2, num_students + 2):
            name_entry = Entry(scrollable_frame, relief="solid", borderwidth=1, width=20)
            name_entry.grid(row=row, column=0, sticky="nsew")
            name_entry.insert(0, f"Студент {row - 1}")
            main_app.student_name_entries.append(name_entry)

            name_entry.bind("<FocusIn>", focus_name_student)
            name_entry.bind("<FocusOut>", unfocus_name_student)

            student_attendance = []
            student_grades = []

            for col in range(1, num_lessons + 1):
                cell_frame = Frame(scrollable_frame, relief="solid", borderwidth=1, width=150)
                cell_frame.grid(row=row, column=col, sticky="nsew")
                cell_frame.grid_propagate(False)

                top_bottom_frame = Frame(cell_frame)
                top_bottom_frame.pack(fill=BOTH, expand=True)

                checkbox_state = {'checked': False}

                def make_toggle(state_dict=checkbox_state, s_idx=row - 2, l_idx=col - 1):
                    def toggle():
                        state_dict['checked'] = not state_dict['checked']

                    return toggle

                attendance_check = Checkbutton(top_bottom_frame, command=make_toggle())
                attendance_check.pack(side=TOP, fill=BOTH, expand=True)

                grade_entry = Entry(top_bottom_frame, width=8)
                grade_entry.pack(side=BOTTOM, fill=X, expand=True)

                student_attendance.append(checkbox_state)
                student_grades.append(grade_entry)

            if has_exam:
                exam_frame = Frame(scrollable_frame, relief="solid", borderwidth=1, width=150)
                exam_frame.grid(row=row, column=num_lessons + 1, sticky="nsew")
                exam_frame.grid_propagate(False)

                exam_entry = Entry(exam_frame, width=12)
                exam_entry.pack(fill=BOTH, expand=True, padx=2, pady=2)
                main_app.exam_entries.append(exam_entry)

            main_app.attendance_vars.append(student_attendance)
            main_app.grade_entries.append(student_grades)

        for i in range(num_students + 2):
            scrollable_frame.grid_rowconfigure(i, weight=1)

        scrollable_frame.grid_columnconfigure(0, minsize=200)
        for i in range(1, num_lessons + 1):
            scrollable_frame.grid_columnconfigure(i, minsize=150)
        if has_exam:
            scrollable_frame.grid_columnconfigure(num_lessons + 1, minsize=150)

        def bind_smart_focus(widget):
            if isinstance(widget, (Frame, Label)):
                widget.bind("<Button-1>", set_focus)
            for child in widget.winfo_children():
                bind_smart_focus(child)

        bind_smart_focus(scrollable_frame)

        h_scrollbar.pack(side=BOTTOM, fill=X)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        v_scrollbar.pack(side=RIGHT, fill=Y)

        legend_frame = Frame(main_app.window7)
        legend_frame.pack(pady=10)
        legend_text = "✓ - отметка присутствия    |    поле ввода - оценка"
        legend_label = Label(legend_frame, text=legend_text, font=("Arial", 10))
        legend_label.pack()

        button_frame = Frame(main_app.window7)
        button_frame.pack(pady=10)
        save_button = Button(button_frame, text="Сохранить", command=lambda: ScheduleWindows.save_table_data(main_app))
        save_button.pack(side=LEFT, padx=10)
        back_button = Button(button_frame, text="Назад", command=lambda: ScheduleWindows.back_from_window7(main_app))
        back_button.pack(side=LEFT, padx=10)
        exit_button = Button(button_frame, text="Выход", command=main_app.exit_program)
        exit_button.pack(side=LEFT, padx=10)

        canvas.focus_set()
        window.mainloop()

    @staticmethod
    def save_table_data(main_app):
        try:
            subject_name = main_app.object_entry.get()
            has_exam = main_app.has_exam
            num_lessons = len(main_app.date_entries)
            num_students = len(main_app.student_name_entries)

            main_app.cursor.execute("INSERT INTO subjects (name, has_exam) VALUES (?, ?)",
                                    (subject_name, has_exam))
            subject_id = main_app.cursor.lastrowid

            if has_exam and hasattr(main_app, 'exam_date_entry'):
                main_app.cursor.execute('''
                    INSERT INTO schedules(subject_id, lesson_number, date, lab_work)
                    VALUES(?, ?, ?, ?)
                ''', (subject_id, 0, main_app.exam_date_entry.get(), "Экзамен"))

            schedule_ids = []
            for i, (date_entry, lab_entry) in enumerate(zip(main_app.date_entries, main_app.lab_entries)):
                main_app.cursor.execute('''
                    INSERT INTO schedules(subject_id, lesson_number, date, lab_work)
                    VALUES(?, ?, ?, ?)
                ''', (subject_id, i + 1, date_entry.get(), lab_entry.get()))
                schedule_ids.append(main_app.cursor.lastrowid)

            student_ids = []
            for student_idx, name_entry in enumerate(main_app.student_name_entries):
                display_name = name_entry.get()
                global_student_name = display_name

                main_app.cursor.execute('''
                    SELECT id FROM global_students WHERE student_name = ?
                ''', (global_student_name,))
                existing_global = main_app.cursor.fetchone()

                if existing_global:
                    global_student_id = existing_global[0]
                else:
                    main_app.cursor.execute('''
                        INSERT INTO global_students(student_name) VALUES(?)
                    ''', (global_student_name,))
                    global_student_id = main_app.cursor.lastrowid

                main_app.cursor.execute('''
                    INSERT INTO students(global_student_id, schedule_id, student_row, display_name)
                    VALUES(?, ?, ?, ?)
                ''', (global_student_id, schedule_ids[0], student_idx + 1, display_name))
                student_id = main_app.cursor.lastrowid
                student_ids.append(student_id)

            for lesson_idx in range(num_lessons):
                for student_idx, student_id in enumerate(student_ids):
                    state_dict = main_app.attendance_vars[student_idx][lesson_idx]
                    attendance = state_dict['checked']
                    grade = main_app.grade_entries[student_idx][lesson_idx].get()

                    main_app.cursor.execute('''
                        INSERT INTO attendance(student_id, lesson_number, attendance, grade)
                        VALUES(?, ?, ?, ?)
                    ''', (student_id, lesson_idx + 1, 1 if attendance else 0, grade))

            if has_exam and hasattr(main_app, 'exam_entries'):
                for student_idx, (student_id, exam_entry) in enumerate(zip(student_ids, main_app.exam_entries)):
                    exam_grade = exam_entry.get()
                    main_app.cursor.execute('''
                        INSERT INTO exams(subject_id, student_id, exam_grade)
                        VALUES(?, ?, ?)
                    ''', (subject_id, student_id, exam_grade))

            main_app.conn.commit()
            messagebox.showinfo("Успех", "Расписание сохранено в базу данных")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении: {str(e)}")

    @staticmethod
    def back_from_window6(main_app):
        """Вернуться из окна создания расписания"""
        try:
            if hasattr(main_app, 'window6') and main_app.window6:
                main_app.window6.destroy()
        except:
            pass

        # Создаем новое окно преподавателя
        from windows.teacher_main import TeacherMainWindow
        TeacherMainWindow(main_app)

    @staticmethod
    def back_from_window7(main_app):
        """Вернуться из окна создания таблицы"""
        try:
            if hasattr(main_app, 'window7') and main_app.window7:
                main_app.window7.destroy()
        except:
            pass

        # Показываем окно 6 снова
        if hasattr(main_app, 'window6') and main_app.window6:
            main_app.window6.deiconify()

    @staticmethod
    def show_edit_schedule(main_app):
        if not hasattr(main_app, 'vis_ch'):
            main_app.vis_ch = False

        # Удаляем старые окна перед созданием новых
        for window_attr in ['window8', 'window9', 'window11']:
            if hasattr(main_app, window_attr):
                try:
                    window = getattr(main_app, window_attr)
                    if window:
                        window.destroy()
                except:
                    pass

        # Создаем новое окно
        window = Tk()
        if main_app.vis_ch:
            main_app.window12 = window
            text_m = "Просмотр расписания"
            label_text = "Выберите предмет для просмотра:"
            subjects = ScheduleWindows.get_subjects_for_student(main_app)
        else:
            main_app.window8 = window
            text_m = "Редактирование расписания"
            label_text = "Выберите предмет для редактирования:"
            subjects = ScheduleWindows.get_subjects_from_db(main_app)

        window.title(f"{text_m}")
        window.geometry(f"{main_app.weight}x{main_app.height}")

        select_frame = Frame(window)
        select_frame.pack(pady=20)
        Label(select_frame, text=label_text).pack(pady=10)

        main_app.selected_subject = StringVar(window)
        if subjects:
            main_app.selected_subject.set(subjects[0])
            subject_dropdown = OptionMenu(select_frame, main_app.selected_subject, *subjects)
            subject_dropdown.config(width=30, font=("Arial", 10))
            subject_dropdown.pack(pady=10)

            if main_app.vis_ch:
                cmd = lambda: ScheduleWindows.load_schedule_for_visiting(main_app)
            else:
                cmd = lambda: ScheduleWindows.load_schedule_for_editing(main_app)

            load_button = Button(select_frame, text="Загрузить расписание", command=cmd,
                                 font=("Arial", 12), bg="lightblue")
            load_button.pack(pady=10)

            if not main_app.vis_ch:
                delete_button = Button(select_frame, text="Удалить расписание",
                                       command=lambda: ScheduleWindows.delete_schedule(main_app),
                                       font=("Arial", 12), bg="lightcoral")
                delete_button.pack(pady=5)
        else:
            if main_app.vis_ch:
                Label(select_frame, text="У вас нет доступных расписаний", fg="red").pack(pady=10)
            else:
                Label(select_frame, text="В базе данных нет созданных расписаний", fg="red").pack(pady=10)

        button_frame = Frame(window)
        button_frame.pack(side=BOTTOM, pady=20)

        if main_app.vis_ch:
            back_button = Button(button_frame, text="Назад",
                                 command=lambda: ScheduleWindows.back_to_w5(main_app))
            back_button.pack(side=LEFT, padx=10)
        else:
            back_button = Button(button_frame, text="Назад",
                                 command=lambda: ScheduleWindows.back_to_w4(main_app))
            back_button.pack(side=LEFT, padx=10)

        exit_button = Button(button_frame, text="Выход", command=main_app.exit_program)
        exit_button.pack(side=LEFT, padx=10)

    @staticmethod
    def get_subjects_from_db(main_app):
        try:
            main_app.cursor.execute("SELECT id, name FROM subjects ORDER BY created_date DESC")
            subjects = main_app.cursor.fetchall()
            main_app.subject_ids = {name: id for id, name in subjects}
            return [name for id, name in subjects]
        except Exception as e:
            print(f"Ошибка при получении предметов: {e}")
            return []

    @staticmethod
    def load_schedule_for_editing(main_app):
        selected_subject_name = main_app.selected_subject.get()
        if not selected_subject_name:
            messagebox.showwarning("Внимание", "Выберите предмет для редактирования")
            return

        subject_id = main_app.subject_ids.get(selected_subject_name)
        if not subject_id:
            messagebox.showerror("Ошибка", "Не удалось найти выбранный предмет")
            return

        try:
            # Закрываем окно выбора предмета
            if hasattr(main_app, 'window8') and main_app.window8:
                main_app.window8.destroy()
                main_app.window8 = None
        except:
            pass

        # Открываем редактор
        ScheduleWindows.open_schedule_editor(main_app, subject_id, selected_subject_name)

    @staticmethod
    def open_schedule_editor(main_app, subject_id, subject_name):
        main_app.window9 = Tk()
        main_app.window9.geometry("900x700")
        main_app.window9.title(f"Редактирование: {subject_name}")

        subject_data = ScheduleWindows.load_subject_data(main_app, subject_id)
        if not subject_data:
            messagebox.showerror("Ошибка", "Не удалось загрузить данные расписания")
            main_app.window9.destroy()
            main_app.window4.deiconify()
            return

        ScheduleWindows.show_schedule_editor(main_app, subject_id, subject_name, subject_data)

    @staticmethod
    def load_subject_data(main_app, subject_id):
        try:
            main_app.cursor.execute("SELECT name, has_exam FROM subjects WHERE id=?", (subject_id,))
            subject_info = main_app.cursor.fetchone()

            main_app.cursor.execute('''
                SELECT lesson_number, date, lab_work
                FROM schedules
                WHERE subject_id = ? AND lesson_number > 0
                ORDER BY lesson_number
            ''', (subject_id,))
            schedule_data = main_app.cursor.fetchall()

            main_app.cursor.execute('''
                SELECT date FROM schedules
                WHERE subject_id = ? AND lesson_number = 0
            ''', (subject_id,))
            exam_data = main_app.cursor.fetchone()

            main_app.cursor.execute('''
                SELECT s.id, gs.student_name, s.student_row, s.display_name
                FROM students s
                JOIN global_students gs ON s.global_student_id = gs.id
                WHERE s.schedule_id IN (SELECT id FROM schedules WHERE subject_id = ?)
                ORDER BY s.student_row
            ''', (subject_id,))
            students = main_app.cursor.fetchall()

            student_data = {}
            for student_id, global_name, student_row, display_name in students:
                main_app.cursor.execute('''
                    SELECT lesson_number, attendance, grade
                    FROM attendance
                    WHERE student_id = ?
                    ORDER BY lesson_number
                ''', (student_id,))
                attendance_data = main_app.cursor.fetchall()

                attendance_dict = {}
                grades_dict = {}
                for lesson_num, att, grade in attendance_data:
                    attendance_dict[lesson_num] = bool(att)
                    grades_dict[lesson_num] = grade if grade is not None else ""

                main_app.cursor.execute('''
                    SELECT exam_grade FROM exams
                    WHERE subject_id = ? AND student_id = ?
                ''', (subject_id, student_id))
                exam_result = main_app.cursor.fetchone()

                final_name = display_name if display_name else f"Студент {student_row}"
                exam_grade_value = exam_result[0] if exam_result and exam_result[0] is not None else ""

                student_data[student_id] = {
                    'name': final_name,
                    'row': student_row,
                    'attendance': attendance_dict,
                    'grades': grades_dict,
                    'exam_grade': exam_grade_value
                }

            return {
                'subject_info': subject_info,
                'schedule_data': schedule_data,
                'exam_data': exam_data,
                'student_data': student_data
            }

        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
            return None

    @staticmethod
    def show_schedule_editor(main_app, subject_id, subject_name, subject_data):
        main_app.current_subject_id = subject_id

        if not hasattr(main_app, 'current_sort_mode'):
            main_app.current_sort_mode = 'alphabetical'

        if not hasattr(main_app, 'sche_r'):
            main_app.sche_r = False

        if not hasattr(main_app, 'vis_ch'):
            main_app.vis_ch = False

        if main_app.sche_r:
            window = main_app.window11
            text_message = "Выставление оценок по:"
        elif main_app.vis_ch:
            window = main_app.window11
            text_message = "Просмотр оценок по:"
        else:
            window = main_app.window9
            text_message = "Редактирование:"

        window.title(f"{text_message} {subject_name}")
        window.geometry("900x700")

        for widget in window.winfo_children():
            widget.destroy()

        def validate_grade_input(new_value):
            if new_value == "":
                return True
            try:
                grade = float(new_value)
                return 1 <= grade <= 10
            except ValueError:
                return False

        def on_grade_validate(P):
            return validate_grade_input(P)

        vcmd = (window.register(on_grade_validate), '%P')

        title_label = Label(window, text=f"{text_message} {subject_name}", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        main_container = Frame(window)
        main_container.pack(pady=10, fill=BOTH, expand=True)

        canvas = Canvas(main_container, bg='systemWindowBackgroundColor')
        v_scrollbar = Scrollbar(main_container, orient="vertical", command=canvas.yview, width=20)
        h_scrollbar = Scrollbar(main_container, orient="horizontal", command=canvas.xview, width=20)

        scrollable_frame = Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        def on_canvas_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_arrows(event):
            if event.keysym == 'Up':
                canvas.yview_scroll(-1, "units")
            elif event.keysym == 'Down':
                canvas.yview_scroll(1, "units")
            elif event.keysym == 'Left':
                canvas.xview_scroll(-1, "units")
            elif event.keysym == 'Right':
                canvas.xview_scroll(1, "units")

        def on_mouse_wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def on_shift_wheel(event):
            canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

        def set_focus(event):
            widget = event.widget
            if not isinstance(widget, (Entry, Checkbutton)):
                canvas.focus_set()

        scrollable_frame.bind("<Configure>", on_canvas_configure)
        canvas.bind("<KeyPress>", on_arrows)
        canvas.bind("<Button-1>", set_focus)
        canvas.bind("<MouseWheel>", on_mouse_wheel)
        canvas.bind("<Shift-MouseWheel>", on_shift_wheel)

        num_lessons = len(subject_data['schedule_data'])
        has_exam = subject_data['subject_info'][1]

        student_data = subject_data['student_data']
        if main_app.vis_ch:
            if hasattr(main_app, 'student_id'):
                current_student_id = int(main_app.student_id)
            elif hasattr(main_app, 'id_get') and hasattr(main_app.id_get, 'get'):
                current_student_id = int(main_app.id_get.get())
            else:
                # Если ID не найден, выводим ошибку
                messagebox.showerror("Ошибка", "ID студента не найден")
                window.destroy()
                if main_app.vis_ch:
                    from windows.student_window import StudentWindow
                    StudentWindow(main_app)
                return
            filtered_student_data = {}

            for student_id, data in student_data.items():
                main_app.cursor.execute('SELECT global_student_id FROM students WHERE id = ?', (student_id,))
                result = main_app.cursor.fetchone()
                if result and result[0] == current_student_id:
                    filtered_student_data[student_id] = data
                    break

            if not filtered_student_data:
                messagebox.showerror("Ошибка", "Студент не найден в этом расписании")
                window.destroy()
                main_app.window5.deiconify()
                return

            student_data = filtered_student_data
            num_students = 1
        else:
            num_students = len(student_data)

        student_list = []
        for student_id, data in student_data.items():
            student_list.append({
                'id': student_id,
                'name': data['name'],
                'attendance': data['attendance'],
                'grades': data['grades'],
                'exam_grade': data['exam_grade'],
                'row': data.get('row', 0)
            })

        student_list.sort(key=lambda x: x['row'])

        headers = ["Студенты"] + [f"Занятие {i + 1}" for i in range(num_lessons)]
        if has_exam:
            headers.append("Экзамен")

        for col, header in enumerate(headers):
            width = 20 if col == 0 else 12
            header_label = Label(scrollable_frame, text=header, relief="solid", borderwidth=1,
                                 width=width, height=2, bg="lightgray")
            header_label.grid(row=0, column=col, sticky="nsew")

        Label(scrollable_frame, text="Дата/Лаб.раб.", relief="solid", borderwidth=1,
              bg="lightblue", width=20).grid(row=1, column=0, sticky="nsew")

        main_app.date_entries = []
        main_app.lab_entries = []

        for col, (lesson_num, date, lab_work) in enumerate(subject_data['schedule_data'], 1):
            entry_frame = Frame(scrollable_frame, relief="solid", borderwidth=1, width=120)
            entry_frame.grid(row=1, column=col, sticky="nsew")
            entry_frame.grid_propagate(False)

            date_entry = Entry(entry_frame, width=10)
            date_entry.pack(side=TOP, fill=X, padx=2, pady=1)

            lab_entry = Entry(entry_frame, width=10)
            lab_entry.pack(side=BOTTOM, fill=X, padx=2, pady=1)

            if date:
                date_entry.insert(0, date)
            else:
                date_entry.insert(0, f"Дата {col}")

            if lab_work:
                lab_entry.insert(0, lab_work)
            else:
                lab_entry.insert(0, "Лаб.раб.")

            if main_app.sche_r or main_app.vis_ch:
                date_entry.config(state="readonly")
                lab_entry.config(state="readonly")

            main_app.date_entries.append(date_entry)
            main_app.lab_entries.append(lab_entry)

        if has_exam and subject_data['exam_data']:
            exam_date_frame = Frame(scrollable_frame, relief="solid", borderwidth=1, width=120)
            exam_date_frame.grid(row=1, column=num_lessons + 1, sticky="nsew")
            exam_date_frame.grid_propagate(False)

            exam_date_entry = Entry(exam_date_frame, width=10)
            exam_date_entry.pack(side=TOP, fill=X, padx=2, pady=1)
            exam_date_entry.insert(0, subject_data['exam_data'][0])

            if main_app.sche_r or main_app.vis_ch:
                exam_date_entry.config(state="readonly")
            main_app.exam_date_entry = exam_date_entry

        main_app.student_name_entries = []
        main_app.attendance_vars = []
        main_app.grade_entries = []
        main_app.exam_entries = []

        def focus_name_student(event):
            if not main_app.vis_ch:
                system_bg = window.cget('bg')
                for entry in main_app.student_name_entries:
                    entry.configure(highlightbackground=system_bg, highlightthickness=1)
                for row in range(2, num_students + 2):
                    for col in range(len(headers)):
                        cells = scrollable_frame.grid_slaves(row=row, column=col)
                        if cells:
                            cells[0].configure(highlightbackground=system_bg, highlightthickness=1)

                event.widget.configure(highlightbackground="#FFDAB9", highlightthickness=1)
                row = event.widget.grid_info()['row']
                for col in range(len(headers)):
                    cells = scrollable_frame.grid_slaves(row=row, column=col)
                    if cells:
                        cells[0].configure(highlightbackground="#FFDAB9", highlightthickness=1)

        def unfocus_name_student(event):
            if not main_app.vis_ch:
                system_bg = window.cget('bg')
                row = event.widget.grid_info()['row']
                event.widget.configure(highlightbackground=system_bg, highlightthickness=1)
                for col in range(len(headers)):
                    cells = scrollable_frame.grid_slaves(row=row, column=col)
                    if cells:
                        cells[0].configure(highlightbackground=system_bg, highlightthickness=1)

        for idx, student in enumerate(student_list):
            row = idx + 2

            name_entry = Entry(scrollable_frame, relief="solid", borderwidth=1, width=20)
            name_entry.grid(row=row, column=0, sticky="nsew")
            name_entry.insert(0, student['name'])
            name_entry.bind("<FocusIn>", focus_name_student)
            name_entry.bind("<FocusOut>", unfocus_name_student)

            if main_app.sche_r or main_app.vis_ch:
                name_entry.config(state="readonly")

            main_app.student_name_entries.append(name_entry)

            student_attendance = []
            student_grades = []

            for col in range(1, num_lessons + 1):
                cell_frame = Frame(scrollable_frame, relief="solid", borderwidth=1, width=120)
                cell_frame.grid(row=row, column=col, sticky="nsew")
                cell_frame.grid_propagate(False)

                top_bottom_frame = Frame(cell_frame)
                top_bottom_frame.pack(fill=BOTH, expand=True)

                attendance_value = student['attendance'].get(col, False)
                checkbox_state = {'checked': attendance_value}

                def make_toggle(state_dict=checkbox_state):
                    def toggle():
                        if not main_app.vis_ch:
                            state_dict['checked'] = not state_dict['checked']

                    return toggle

                attendance_check = Checkbutton(top_bottom_frame, command=make_toggle())
                attendance_check.pack(side=TOP, fill=BOTH, expand=True)

                if attendance_value:
                    attendance_check.select()
                else:
                    attendance_check.deselect()

                grade_value = student['grades'].get(col, "")
                grade_entry = Entry(top_bottom_frame, width=6, validate="key", validatecommand=vcmd)
                grade_entry.pack(side=BOTTOM, fill=X, expand=True)
                grade_entry.insert(0, grade_value)

                if main_app.vis_ch:
                    attendance_check.config(state="disabled")
                    grade_entry.config(state="readonly")

                student_attendance.append(checkbox_state)
                student_grades.append(grade_entry)

            if has_exam:
                exam_frame = Frame(scrollable_frame, relief="solid", borderwidth=1, width=120)
                exam_frame.grid(row=row, column=num_lessons + 1, sticky="nsew")
                exam_frame.grid_propagate(False)

                exam_entry = Entry(exam_frame, width=8, validate="key", validatecommand=vcmd)
                exam_entry.pack(fill=BOTH, expand=True, padx=2, pady=2)
                exam_entry.insert(0, student['exam_grade'] or "")

                if main_app.vis_ch:
                    exam_entry.config(state="readonly")

                main_app.exam_entries.append(exam_entry)

            main_app.attendance_vars.append(student_attendance)
            main_app.grade_entries.append(student_grades)

        for i in range(num_students + 2):
            scrollable_frame.grid_rowconfigure(i, weight=1)

        scrollable_frame.grid_columnconfigure(0, minsize=200)
        for i in range(1, num_lessons + 1):
            scrollable_frame.grid_columnconfigure(i, minsize=120)
        if has_exam:
            scrollable_frame.grid_columnconfigure(num_lessons + 1, minsize=120)

        def bind_smart_focus(widget):
            if isinstance(widget, (Frame, Label)):
                widget.bind("<Button-1>", set_focus)
            for child in widget.winfo_children():
                bind_smart_focus(child)

        bind_smart_focus(scrollable_frame)

        h_scrollbar.pack(side=BOTTOM, fill=X)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        v_scrollbar.pack(side=RIGHT, fill=Y)

        legend_frame = Frame(window)
        legend_frame.pack(pady=10)
        if main_app.vis_ch:
            legend_text = "Режим просмотра - данные только для чтения"
        else:
            legend_text = "✓ - отметка присутствия | поле ввода - оценка (1-10)"

        legend_label = Label(legend_frame, text=legend_text, font=("Arial", 10))
        legend_label.pack()

        button_frame = Frame(window)
        button_frame.pack(pady=10)

        # Функция проверки всех оценок перед сохранением
        def validate_all_grades():
            all_valid = True
            invalid_fields = []

            # Проверяем обычные оценки
            for row, grade_entries in enumerate(main_app.grade_entries, 1):
                for col, grade_entry in enumerate(grade_entries, 1):
                    value = grade_entry.get().strip()
                    if value and not validate_grade_input(value):
                        all_valid = False
                        student_name = main_app.student_name_entries[row - 1].get()
                        invalid_fields.append(f"{student_name}, занятие {col}: '{value}'")

            # Проверяем экзаменационные оценки
            for row, exam_entry in enumerate(main_app.exam_entries, 1):
                value = exam_entry.get().strip()
                if value and not validate_grade_input(value):
                    all_valid = False
                    student_name = main_app.student_name_entries[row - 1].get()
                    invalid_fields.append(f"{student_name}, экзамен: '{value}'")

            return all_valid, invalid_fields

        # Модифицируем функцию сохранения
        def safe_save_edited_schedule(subj_id):
            all_valid, invalid_fields = validate_all_grades()
            if not all_valid:
                error_msg = "Обнаружены некорректные оценки (допустимо 1-10):\n" + "\n".join(invalid_fields)
                messagebox.showerror("Ошибка ввода", error_msg)
                return
            ScheduleWindows.save_edited_schedule(main_app, subj_id)

        # Сначала кнопки для РЕДАКТИРОВАНИЯ (только когда sche_r = False и не студент)
        if not main_app.vis_ch:
            # Кнопка сохранения для обоих режимов преподавателя
            save_button = Button(button_frame, text="Сохранить",
                                 command=lambda: safe_save_edited_schedule(subject_id),
                                 font=("Arial", 12), bg="lightgreen")
            save_button.pack(side=LEFT, padx=10)

            # Кнопки удаления ТОЛЬКО для режима РЕДАКТИРОВАНИЯ (не для выставления оценок)
            if not main_app.sche_r:
                delete_student_btn = Button(button_frame, text="Удалить студента",
                                            command=lambda: ScheduleWindows.delete_student(main_app, subject_id),
                                            font=("Arial", 12), bg="lightcoral")
                delete_student_btn.pack(side=LEFT, padx=10)

                delete_lesson_btn = Button(button_frame, text="Удалить занятие",
                                           command=lambda: ScheduleWindows.delete_lesson(main_app, subject_id),
                                           font=("Arial", 12), bg="lightcoral")
                delete_lesson_btn.pack(side=LEFT, padx=10)

        # Кнопка сортировки для ВСЕХ режимов преподавателя (редактирование и выставление оценок)
        if not main_app.vis_ch:  # Если не студент
            def update_sort_button_text():
                if not hasattr(main_app, 'current_sort_mode'):
                    main_app.current_sort_mode = 'alphabetical'

                if main_app.current_sort_mode == 'alphabetical':
                    return "Сортировать по успеваемости"
                else:
                    return "Сортировать по алфавиту"

            sort_by_marks_btn = Button(button_frame,
                                       text=update_sort_button_text(),
                                       command=lambda: ScheduleWindows.sort_by_marks_func(main_app),
                                       font=("Arial", 12),
                                       bg="lightblue")
            sort_by_marks_btn.pack(side=LEFT, padx=10)

            main_app.sort_button = sort_by_marks_btn

        if main_app.sche_r:
            back_button_cmd = lambda: ScheduleWindows.back_to_w10(main_app)
        else:
            back_button_cmd = lambda: ScheduleWindows.back_to_edit_list(main_app)

        back_button = Button(button_frame, text="Назад", command=back_button_cmd)
        back_button.pack(side=LEFT, padx=10)
        exit_button = Button(button_frame, text="Выход", command=main_app.exit_program)
        exit_button.pack(side=LEFT, padx=10)

        canvas.focus_set()

    @staticmethod
    def save_edited_schedule(main_app, subject_id):
        try:
            for i, (date_entry, lab_entry) in enumerate(zip(main_app.date_entries, main_app.lab_entries)):
                main_app.cursor.execute('''
                    UPDATE schedules SET date = ?, lab_work = ?
                    WHERE subject_id = ? AND lesson_number = ?
                ''', (date_entry.get(), lab_entry.get(), subject_id, i + 1))

            if hasattr(main_app, 'exam_date_entry'):
                main_app.cursor.execute('''
                    UPDATE schedules SET date = ?
                    WHERE subject_id = ? AND lesson_number = 0
                ''', (main_app.exam_date_entry.get(), subject_id))

            main_app.cursor.execute('''
                SELECT s.id, s.global_student_id, s.student_row, s.display_name
                FROM students s
                WHERE s.schedule_id IN (SELECT id FROM schedules WHERE subject_id = ?)
                ORDER BY s.student_row
            ''', (subject_id,))
            students = main_app.cursor.fetchall()

            for student_idx, (student_id, current_global_id, student_row, current_display_name) in enumerate(students):
                if student_idx < len(main_app.student_name_entries):
                    new_display_name = main_app.student_name_entries[student_idx].get()

                    if new_display_name != current_display_name:
                        main_app.cursor.execute('SELECT id FROM global_students WHERE student_name = ?',
                                                (new_display_name,))
                        existing_global = main_app.cursor.fetchone()

                        if existing_global:
                            new_global_id = existing_global[0]
                            main_app.cursor.execute('''
                                UPDATE students SET global_student_id = ?, display_name = ?
                                WHERE id = ?
                            ''', (new_global_id, new_display_name, student_id))

                            main_app.cursor.execute('SELECT COUNT(*) FROM students WHERE global_student_id = ?',
                                                    (current_global_id,))
                            remaining_links = main_app.cursor.fetchone()[0]
                            if remaining_links == 0:
                                main_app.cursor.execute('DELETE FROM global_students WHERE id = ?', (current_global_id,))
                        else:
                            main_app.cursor.execute('INSERT INTO global_students(student_name) VALUES(?)',
                                                    (new_display_name,))
                            new_global_id = main_app.cursor.lastrowid
                            main_app.cursor.execute('''
                                UPDATE students SET global_student_id = ?, display_name = ?
                                WHERE id = ?
                            ''', (new_global_id, new_display_name, student_id))

                            main_app.cursor.execute('SELECT COUNT(*) FROM students WHERE global_student_id = ?',
                                                    (current_global_id,))
                            remaining_links = main_app.cursor.fetchone()[0]
                            if remaining_links == 0:
                                main_app.cursor.execute('DELETE FROM global_students WHERE id = ?', (current_global_id,))
                    else:
                        main_app.cursor.execute('UPDATE students SET display_name = ? WHERE id = ?',
                                                (new_display_name, student_id))

            for student_idx, (student_id, global_student_id, student_row, display_name) in enumerate(students):
                if student_idx < len(main_app.attendance_vars):
                    for lesson_idx, state_dict in enumerate(main_app.attendance_vars[student_idx]):
                        attendance = state_dict['checked']
                        grade = main_app.grade_entries[student_idx][lesson_idx].get()

                        main_app.cursor.execute('''
                            SELECT id FROM attendance
                            WHERE student_id = ? AND lesson_number = ?
                        ''', (student_id, lesson_idx + 1))
                        existing_attendance = main_app.cursor.fetchone()

                        if existing_attendance:
                            main_app.cursor.execute('''
                                UPDATE attendance
                                SET attendance = ?, grade = ?
                                WHERE student_id = ? AND lesson_number = ?
                            ''', (1 if attendance else 0, grade, student_id, lesson_idx + 1))
                        else:
                            main_app.cursor.execute('''
                                INSERT INTO attendance(student_id, lesson_number, attendance, grade)
                                VALUES(?, ?, ?, ?)
                            ''', (student_id, lesson_idx + 1, 1 if attendance else 0, grade))

            if hasattr(main_app, 'exam_entries'):
                for student_idx, (student_id, global_student_id, student_row, display_name) in enumerate(students):
                    if student_idx < len(main_app.exam_entries):
                        exam_grade = main_app.exam_entries[student_idx].get()
                        main_app.cursor.execute('''
                            SELECT id FROM exams
                            WHERE subject_id = ? AND student_id = ?
                        ''', (subject_id, student_id))
                        existing_exam = main_app.cursor.fetchone()

                        if existing_exam:
                            main_app.cursor.execute('''
                                UPDATE exams SET exam_grade = ?
                                WHERE subject_id = ? AND student_id = ?
                            ''', (exam_grade, subject_id, student_id))
                        else:
                            main_app.cursor.execute('''
                                INSERT INTO exams(subject_id, student_id, exam_grade)
                                VALUES(?, ?, ?)
                            ''', (subject_id, student_id, exam_grade))

            main_app.conn.commit()
            messagebox.showinfo("Успех", "Изменения сохранены")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении: {str(e)}")

    @staticmethod
    def delete_student(main_app, subject_id):
        try:
            main_app.cursor.execute('''
                SELECT s.id, s.display_name
                FROM students s
                WHERE s.schedule_id IN (SELECT id FROM schedules WHERE subject_id = ?)
                ORDER BY s.student_row
            ''', (subject_id,))
            students = main_app.cursor.fetchall()

            if not students:
                messagebox.showwarning("Внимание", "В расписании нет студентов для удаления")
                return

            select_window = Tk()
            select_window.title("Удаление студента")
            select_window.geometry("300x200")

            Label(select_window, text="Выберите студента для удаления:", font=("Arial", 12)).pack(pady=10)
            student_var = StringVar(select_window)
            student_names = [name for id, name in students]
            student_var.set(student_names[0])

            student_dropdown = OptionMenu(select_window, student_var, *student_names)
            student_dropdown.config(width=25, font=("Arial", 10))
            student_dropdown.pack(pady=10)

            def confirm_delete():
                selected_name = student_var.get()
                student_id = None
                for sid, sname in students:
                    if sname == selected_name:
                        student_id = sid
                        break

                if student_id is None:
                    messagebox.showerror("Ошибка", "Не удалось найти ID студента")
                    return

                result = messagebox.askyesno("Подтверждение",
                                             f"Вы уверены, что хотите удалить студента '{selected_name}'?")
                if result:
                    main_app.cursor.execute("DELETE FROM attendance WHERE student_id = ?", (student_id,))
                    main_app.cursor.execute("DELETE FROM exams WHERE student_id = ?", (student_id,))

                    main_app.cursor.execute('SELECT global_student_id FROM students WHERE id = ?', (student_id,))
                    global_student_id = main_app.cursor.fetchone()[0]

                    main_app.cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))

                    main_app.cursor.execute('SELECT COUNT(*) FROM students WHERE global_student_id = ?',
                                            (global_student_id,))
                    remaining_links = main_app.cursor.fetchone()[0]
                    if remaining_links == 0:
                        main_app.cursor.execute('DELETE FROM global_students WHERE id = ?', (global_student_id,))

                    main_app.conn.commit()
                    messagebox.showinfo("Успех", f"Студент '{selected_name}' удален")
                    select_window.destroy()
                    ScheduleWindows.refresh_editor(main_app, subject_id)

            Button(select_window, text="Удалить", command=confirm_delete,
                   font=("Arial", 12), bg="lightcoral").pack(pady=10)
            Button(select_window, text="Отмена", command=select_window.destroy,
                   font=("Arial", 12)).pack(pady=5)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при удалении студента: {str(e)}")

    @staticmethod
    def delete_lesson(main_app, subject_id):
        try:
            main_app.cursor.execute('''
                SELECT lesson_number, date, lab_work
                FROM schedules
                WHERE subject_id = ? AND lesson_number > 0
                ORDER BY lesson_number
            ''', (subject_id,))
            lessons = main_app.cursor.fetchall()

            if not lessons:
                messagebox.showwarning("Внимание", "В расписании нет занятий для удаления")
                return

            if len(lessons) == 1:
                messagebox.showwarning("Внимание", "Нельзя удалить единственное занятие в расписании")
                return

            select_window = Tk()
            select_window.title("Удаление занятия")
            select_window.geometry("400x250")

            Label(select_window, text="Выберите занятие для удаления:", font=("Arial", 12)).pack(pady=10)
            lesson_var = StringVar(select_window)
            lesson_options = [f"Занятие {num}: {date} ({lab})" for num, date, lab in lessons]
            lesson_var.set(lesson_options[0])

            lesson_dropdown = OptionMenu(select_window, lesson_var, *lesson_options)
            lesson_dropdown.config(width=35, font=("Arial", 10))
            lesson_dropdown.pack(pady=10)

            def confirm_delete():
                selected_text = lesson_var.get()
                lesson_number = int(selected_text.split("Занятие ")[1].split(":")[0])

                result = messagebox.askyesno("Подтверждение",
                                             f"Вы уверены, что хотите удалить занятие {lesson_number}?")
                if result:
                    main_app.cursor.execute('''
                        DELETE FROM attendance
                        WHERE lesson_number = ? AND student_id IN(
                            SELECT s.id FROM students s
                            JOIN schedules sch ON s.schedule_id = sch.id
                            WHERE sch.subject_id = ?
                        )
                    ''', (lesson_number, subject_id))

                    if lesson_number == 1:
                        main_app.cursor.execute('''
                            SELECT id FROM schedules
                            WHERE subject_id = ? AND lesson_number > 1
                            ORDER BY lesson_number
                            LIMIT 1
                        ''', (subject_id,))
                        next_lesson = main_app.cursor.fetchone()
                        if next_lesson:
                            main_app.cursor.execute('''
                                UPDATE students
                                SET schedule_id = ?
                                WHERE schedule_id IN(
                                    SELECT id FROM schedules
                                    WHERE subject_id = ? AND lesson_number = 1
                                )
                            ''', (next_lesson[0], subject_id))

                    main_app.cursor.execute('DELETE FROM schedules WHERE subject_id = ? AND lesson_number = ?',
                                            (subject_id, lesson_number))

                    main_app.cursor.execute('''
                        SELECT lesson_number FROM schedules
                        WHERE subject_id = ? AND lesson_number > ?
                        ORDER BY lesson_number
                    ''', (subject_id, lesson_number))
                    later_lessons = main_app.cursor.fetchall()

                    for old_num, in later_lessons:
                        new_num = old_num - 1
                        main_app.cursor.execute('''
                            UPDATE schedules SET lesson_number = ?
                            WHERE subject_id = ? AND lesson_number = ?
                        ''', (new_num, subject_id, old_num))

                        main_app.cursor.execute('''
                            UPDATE attendance SET lesson_number = ?
                            WHERE lesson_number = ? AND student_id IN(
                                SELECT s.id FROM students s
                                JOIN schedules sch ON s.schedule_id = sch.id
                                WHERE sch.subject_id = ?
                            )
                        ''', (new_num, old_num, subject_id))

                    main_app.conn.commit()
                    messagebox.showinfo("Успех", f"Занятие {lesson_number} удалено")
                    select_window.destroy()
                    ScheduleWindows.refresh_editor(main_app, subject_id)

            button_frame = Frame(select_window)
            button_frame.pack(pady=20)
            Button(button_frame, text="Отмена", command=select_window.destroy,
                   font=("Arial", 12)).pack(side=LEFT, padx=10)
            Button(button_frame, text="Удалить", command=confirm_delete,
                   font=("Arial", 12), bg="lightcoral").pack(side=LEFT, padx=10)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при удалении занятия: {str(e)}")

    @staticmethod
    def refresh_editor(main_app, subject_id):
        try:
            main_app.cursor.execute("SELECT name FROM subjects WHERE id = ?", (subject_id,))
            subject_name = main_app.cursor.fetchone()[0]
            subject_data = ScheduleWindows.load_subject_data(main_app, subject_id)

            if not subject_data:
                messagebox.showerror("Ошибка", "Не удалось загрузить обновленные данные")
                return

            if hasattr(main_app, 'window9') and main_app.window9:
                main_app.window9.destroy()
                ScheduleWindows.open_schedule_editor(main_app, subject_id, subject_name)
            elif hasattr(main_app, 'window11') and main_app.window11.winfo_exists():
                main_app.window11.destroy()
                ScheduleWindows.open_schedule_rating(main_app, subject_id, subject_name)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при обновлении редактора: {str(e)}")

    @staticmethod
    def back_to_edit_list(main_app):
        """Вернуться к списку расписаний"""
        # Закрываем текущие окна
        for window_attr in ['window9', 'window11']:
            if hasattr(main_app, window_attr):
                try:
                    window = getattr(main_app, window_attr)
                    if window:
                        window.destroy()
                    setattr(main_app, window_attr, None)
                except:
                    pass

        # Показываем окно выбора расписания
        ScheduleWindows.show_edit_schedule(main_app)

    @staticmethod
    def delete_schedule(main_app):
        selected_subject_name = main_app.selected_subject.get()
        if not selected_subject_name:
            messagebox.showwarning("Внимание", "Выберите предмет для удаления")
            return

        subject_id = main_app.subject_ids.get(selected_subject_name)
        if not subject_id:
            return

        result = messagebox.askyesno("Подтверждение",
                                     f"Вы уверены, что хотите удалить расписание '{selected_subject_name}'?")
        if result:
            try:
                main_app.cursor.execute('''
                    SELECT s.id
                    FROM students s
                    WHERE s.schedule_id IN (SELECT id FROM schedules WHERE subject_id = ?)
                ''', (subject_id,))
                student_ids = [row[0] for row in main_app.cursor.fetchall()]

                main_app.cursor.execute("DELETE FROM exams WHERE subject_id = ?", (subject_id,))

                if student_ids:
                    placeholders = ','.join('?' for _ in student_ids)
                    main_app.cursor.execute(f'DELETE FROM attendance WHERE student_id IN ({placeholders})', student_ids)

                main_app.cursor.execute('''
                    DELETE FROM students
                    WHERE schedule_id IN (SELECT id FROM schedules WHERE subject_id = ?)
                ''', (subject_id,))

                main_app.cursor.execute('''
                    DELETE FROM global_students
                    WHERE id NOT IN (SELECT DISTINCT global_student_id FROM students)
                ''')

                main_app.cursor.execute("DELETE FROM schedules WHERE subject_id = ?", (subject_id,))
                main_app.cursor.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))

                main_app.conn.commit()

                main_app.cursor.execute("SELECT COUNT(*) FROM subjects WHERE id = ?", (subject_id,))
                remaining = main_app.cursor.fetchone()[0]

                if remaining == 0:
                    messagebox.showinfo("Успех", "Расписание удалено")
                else:
                    messagebox.showerror("Ошибка", "Не удалось полностью удалить расписание")

                main_app.window8.destroy()
                ScheduleWindows.show_edit_schedule(main_app)

            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при удалении: {str(e)}")

    @staticmethod
    def back_to_w4(main_app):
        """Вернуться к окну 4"""
        try:
            if hasattr(main_app, 'window8'):
                main_app.window8.destroy()
        except:
            pass

        # Всегда создаем новое окно
        from windows.teacher_main import TeacherMainWindow
        TeacherMainWindow(main_app)

    @staticmethod
    def show_rate_schedule(main_app):
        main_app.window10 = Tk()
        main_app.window10.geometry(f"{main_app.weight}x{main_app.height}")
        main_app.window10.title("Выберите расписание")
        main_app.sche_r = False

        Label(main_app.window10, text="Выставление оценок", font=("Arial", 16, "bold")).pack(pady=20)

        select_frame = Frame(main_app.window10)
        select_frame.pack(pady=20)
        Label(select_frame, text="Выберите предмет для работы:").pack(pady=10)

        subjects = ScheduleWindows.get_subjects_from_db(main_app)
        main_app.selected_subject = StringVar(main_app.window10)

        if subjects:
            main_app.selected_subject.set(subjects[0])
            subject_dropdown = OptionMenu(select_frame, main_app.selected_subject, *subjects)
            subject_dropdown.config(width=30, font=("Arial", 10))
            subject_dropdown.pack(pady=10)

            load_button = Button(select_frame, text="Загрузить расписание",
                                 command=lambda: ScheduleWindows.load_schedule_for_rating(main_app),
                                 font=("Arial", 12), bg="lightblue")
            load_button.pack(pady=10)
        else:
            Label(select_frame, text="В базе данных нет созданных расписаний", fg="red").pack(pady=10)

        button_frame = Frame(main_app.window10)
        button_frame.pack(side=BOTTOM, pady=20)
        Button(button_frame, text="Назад", command=lambda: ScheduleWindows.back_from_w10(main_app)).pack(side=LEFT, padx=10)
        Button(button_frame, text="Выход", command=main_app.exit_program).pack(side=LEFT, padx=10)

    @staticmethod
    def load_schedule_for_rating(main_app):
        selected_subject_name = main_app.selected_subject.get()
        if not selected_subject_name:
            messagebox.showwarning("Внимание", "Выберите предмет для выставления оценок")
            return

        subject_id = main_app.subject_ids.get(selected_subject_name)
        if not subject_id:
            messagebox.showerror("Ошибка", "Не удалось найти выбранный предмет")
            return

        main_app.window10.destroy()
        main_app.sche_r = True
        ScheduleWindows.open_schedule_rating(main_app, subject_id, selected_subject_name)

    @staticmethod
    def open_schedule_rating(main_app, subject_id, subject_name):
        main_app.window11 = Tk()
        main_app.window11.geometry("900x700")

        if not hasattr(main_app, 'vis_ch'):
            main_app.vis_ch = False

        if main_app.vis_ch:
            mes_t = "Просмотр расписания"
        else:
            mes_t = "Выставление оценок"

        main_app.window11.title(f"{mes_t}: {subject_name}")
        subject_data = ScheduleWindows.load_subject_data(main_app, subject_id)

        if not subject_data:
            messagebox.showerror("Ошибка", "Не удалось загрузить данные расписания")
            main_app.window11.destroy()
            if not main_app.vis_ch:
                main_app.window4.deiconify()
            else:
                main_app.window5.deiconify()
            return

        ScheduleWindows.show_schedule_editor(main_app, subject_id, subject_name, subject_data)

    @staticmethod
    def back_from_w10(main_app):
        """Вернуться из окна выставления оценок"""
        try:
            if hasattr(main_app, 'window10') and main_app.window10:
                main_app.window10.destroy()
        except:
            pass

        # Всегда создаем новое окно преподавателя
        from windows.teacher_main import TeacherMainWindow
        TeacherMainWindow(main_app)

    @staticmethod
    def back_to_w10(main_app):
        """Вернуться к выбору предмета для выставления оценок"""
        try:
            if hasattr(main_app, 'window11') and main_app.window11:
                try:
                    main_app.window11.destroy()
                except:
                    pass
        except:
            pass

        # Создаем новое окно выбора
        ScheduleWindows.show_rate_schedule(main_app)

    @staticmethod
    def load_schedule_for_visiting(main_app):
        selected_subject_name = main_app.selected_subject.get()
        if not selected_subject_name:
            messagebox.showwarning("Внимание", "Выберите предмет для просмотра")
            return

        subject_id = main_app.subject_ids.get(selected_subject_name)
        if not subject_id:
            messagebox.showerror("Ошибка", "Не удалось найти выбранный предмет")
            return

        main_app.window12.destroy()
        ScheduleWindows.open_schedule_rating(main_app, subject_id, selected_subject_name)

    @staticmethod
    def back_to_w5(main_app):
        """Вернуться к окну студента"""
        # Закрываем текущее окно
        if hasattr(main_app, 'window12') and main_app.window12:
            main_app.window12.destroy()

        # Создаем новое окно студента
        from windows.student_window import StudentWindow
        StudentWindow(main_app)

    @staticmethod
    def get_subjects_for_student(main_app):
        """Получить предметы, в которых есть текущий студент"""
        try:
            # Получаем student_id из main_app
            if not hasattr(main_app, 'student_id') or not main_app.student_id:
                return []

            student_id = main_app.student_id

            main_app.cursor.execute('''
                SELECT DISTINCT sub.name, sub.id
                FROM subjects sub
                JOIN schedules sch ON sub.id = sch.subject_id
                JOIN students stu ON sch.id = stu.schedule_id
                WHERE stu.global_student_id = ?
                ORDER BY sub.name
            ''', (student_id,))
            subjects = main_app.cursor.fetchall()
            main_app.subject_ids = {name: id for name, id in subjects}
            return [name for name, id in subjects]
        except Exception as e:
            print(f"Ошибка при получении предметов студента: {e}")
            return []

    @staticmethod
    def sort_by_marks_func(main_app):
        # Проверяем, есть ли subject_id
        if not hasattr(main_app, 'current_subject_id') or not main_app.current_subject_id:
            messagebox.showerror("Ошибка", "Не выбран предмет для сортировки")
            return

        # Загружаем данные из базы (а не из памяти)
        try:
            main_app.cursor.execute("SELECT name FROM subjects WHERE id = ?", (main_app.current_subject_id,))
            subject_name_result = main_app.cursor.fetchone()
            if not subject_name_result:
                messagebox.showerror("Ошибка", "Предмет не найден в базе данных")
                return

            subject_name = subject_name_result[0]
            subject_data = ScheduleWindows.load_subject_data(main_app, main_app.current_subject_id)

            if not subject_data:
                messagebox.showerror("Ошибка", "Не удалось загрузить данные для сортировки")
                return

            # Определяем текущий режим сортировки и применяем соответствующую сортировку
            if not hasattr(main_app, 'current_sort_mode'):
                main_app.current_sort_mode = 'alphabetical'

            if main_app.current_sort_mode == 'alphabetical':
                # Если сейчас алфавитная, сортируем по успеваемости
                subject_data['student_data'] = sort_by_marks(subject_data['student_data'])
                main_app.current_sort_mode = 'marks'
                sort_message = "Таблица отсортирована по успеваемости (по убыванию среднего балла)"
            else:
                # Если сейчас сортировка по успеваемости, сортируем по алфавиту
                subject_data['student_data'] = sort_by_alphabet(subject_data['student_data'])
                main_app.current_sort_mode = 'alphabetical'
                sort_message = "Таблица отсортирована по алфавиту"

            # Показываем сообщение о сортировке
            messagebox.showinfo("Сортировка", sort_message)

            # Обновляем отображение таблицы
            ScheduleWindows.refresh_table_with_sorted_data(main_app, subject_data, main_app.current_subject_id)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сортировке: {str(e)}")

    @staticmethod
    def refresh_table_with_sorted_data(main_app, subject_data, subject_id):
        """Обновить таблицу с отсортированными данными"""
        try:
            # Обновляем данные в базе
            ScheduleWindows.save_sorted_order_to_db(main_app, subject_id, subject_data['student_data'])

            # Простая проверка окон без winfo_exists()
            if hasattr(main_app, 'window9') and main_app.window9:
                try:
                    # Закрываем старое окно
                    main_app.window9.destroy()
                except:
                    pass
                # Открываем новое
                main_app.cursor.execute("SELECT name FROM subjects WHERE id = ?", (subject_id,))
                subject_name = main_app.cursor.fetchone()[0]
                ScheduleWindows.open_schedule_editor(main_app, subject_id, subject_name)

            elif hasattr(main_app, 'window11') and main_app.window11:
                try:
                    # Закрываем старое окно
                    main_app.window11.destroy()
                except:
                    pass
                # Открываем новое
                main_app.cursor.execute("SELECT name FROM subjects WHERE id = ?", (subject_id,))
                subject_name = main_app.cursor.fetchone()[0]
                ScheduleWindows.open_schedule_rating(main_app, subject_id, subject_name)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при обновлении таблицы: {str(e)}")

    @staticmethod
    def reopen_window(main_app, subject_id, subject_name, window_type):
        """Переоткрыть окно после сортировки"""
        if window_type == 'edit':
            ScheduleWindows.open_schedule_editor(main_app, subject_id, subject_name)
        elif window_type == 'rate':
            ScheduleWindows.open_schedule_rating(main_app, subject_id, subject_name)

    @staticmethod
    def save_sorted_order_to_db(main_app, subject_id, sorted_student_data):
        """Сохранить отсортированный порядок студентов в базу данных"""
        try:
            for student_id, data in sorted_student_data.items():
                row_number = data['row']
                main_app.cursor.execute('''
                    UPDATE students SET student_row = ?
                    WHERE id = ? AND schedule_id IN (
                        SELECT id FROM schedules WHERE subject_id = ?
                    )
                ''', (row_number, student_id, subject_id))

            main_app.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка сохранения порядка: {e}")
            return False