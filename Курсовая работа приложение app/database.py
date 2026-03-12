import sqlite3
import os
import sys


class Database:
    def __init__(self, db_path='academic_control.db'):
        """
        Инициализация базы данных.

        Args:
            db_path: Относительный путь к файлу базы данных
        """
        # Получаем абсолютный путь к базе данных
        self.db_path = self._get_absolute_db_path(db_path)
        print(f"База данных: {self.db_path}")

        self.conn = None
        self.cursor = None

        # Подключаемся к базе данных
        self.connect()

        # Инициализируем структуру базы данных
        self.init_database_structure()

    def _get_absolute_db_path(self, relative_path):
        """
        Получить абсолютный путь к файлу базы данных.

        Args:
            relative_path: Относительный путь к файлу БД

        Returns:
            str: Абсолютный путь к файлу БД
        """
        # Если запущено из собранного приложения (.app)
        if getattr(sys, 'frozen', False):
            # Режим 1: Приложение собрано с PyInstaller
            # _MEIPASS - папка с ресурсами в .app
            if hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
                print(f"Режим: frozen app, _MEIPASS={base_path}")

                # Проверяем разные возможные расположения БД
                possible_paths = [
                    os.path.join(base_path, relative_path),  # В корне ресурсов
                    os.path.join(base_path, 'Resources', relative_path),  # В папке Resources
                    os.path.join(os.path.dirname(sys.executable), relative_path),  # Рядом с исполняемым файлом
                    os.path.join(os.path.expanduser('~'), relative_path),  # В домашней директории
                ]

                for path in possible_paths:
                    if os.path.exists(path):
                        print(f"Нашел БД: {path}")
                        return path

                # Если БД не найдена, создадим рядом с исполняемым файлом
                app_dir = os.path.dirname(sys.executable)
                return os.path.join(app_dir, relative_path)

            else:
                # Если нет _MEIPASS, используем директорию исполняемого файла
                app_dir = os.path.dirname(sys.executable)
                print(f"Режим: frozen app, app_dir={app_dir}")
                return os.path.join(app_dir, relative_path)

        else:
            # Режим 2: Разработка (исходный код)
            # Определяем базовый путь как директорию, где находится этот файл (database.py)
            base_path = os.path.dirname(os.path.abspath(__file__))
            print(f"Режим: разработка, base_path={base_path}")

            # Пробуем найти БД в разных местах
            possible_paths = [
                os.path.join(base_path, relative_path),  # В той же папке что и database.py
                os.path.join(base_path, '..', relative_path),  # На уровень выше
                os.path.join(os.getcwd(), relative_path),  # В текущей рабочей директории
            ]

            for path in possible_paths:
                path = os.path.normpath(path)  # Нормализуем путь
                if os.path.exists(path):
                    print(f"Нашел БД: {path}")
                    return path

            # Если БД не найдена, создадим в той же папке что и database.py
            return os.path.join(base_path, relative_path)

    def connect(self):
        """Установить соединение с базой данных."""
        try:
            # Создаем директорию для БД если не существует
            db_dir = os.path.dirname(self.db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
                print(f"Создал директорию для БД: {db_dir}")

            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()

            # Включаем поддержку внешних ключей
            self.cursor.execute("PRAGMA foreign_keys = ON")

            print(f"Успешно подключился к БД")
            return self.conn

        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise

    def init_database_structure(self):
        """Инициализировать структуру базы данных."""
        try:
            # Создаем таблицы
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS global_students(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_name TEXT UNIQUE NOT NULL,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS subjects(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    has_exam BOOLEAN DEFAULT 0,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS schedules(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject_id INTEGER,
                    lesson_number INTEGER,
                    date TEXT,
                    lab_work TEXT,
                    FOREIGN KEY(subject_id) REFERENCES subjects(id)
                )
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS students(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    global_student_id INTEGER,
                    schedule_id INTEGER,
                    student_row INTEGER,
                    display_name TEXT,
                    FOREIGN KEY(global_student_id) REFERENCES global_students(id),
                    FOREIGN KEY(schedule_id) REFERENCES schedules(id)
                )
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS attendance(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    lesson_number INTEGER,
                    attendance BOOLEAN DEFAULT 0,
                    grade TEXT,
                    FOREIGN KEY(student_id) REFERENCES students(id)
                )
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS exams(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject_id INTEGER,
                    student_id INTEGER,
                    exam_grade TEXT,
                    FOREIGN KEY(subject_id) REFERENCES subjects(id),
                    FOREIGN KEY(student_id) REFERENCES students(id)
                )
            ''')

            self.conn.commit()
            print("Структура базы данных создана/проверена")

        except Exception as e:
            print(f"Ошибка создания структуры базы данных: {e}")
            self.conn.rollback()
            raise

    def disconnect(self):
        """Закрыть соединение с базой данных."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            print("Соединение с БД закрыто")

    def execute_query(self, query, params=()):
        """Выполнить SQL запрос."""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            self.conn.rollback()
            raise

    def get_all_subjects(self):
        """Получить все предметы."""
        self.cursor.execute("SELECT id, name FROM subjects ORDER BY name")
        return self.cursor.fetchall()

    def get_student_by_id(self, student_id):
        """Получить студента по ID."""
        self.cursor.execute('''
            SELECT gs.id, gs.student_name, s.display_name 
            FROM global_students gs
            LEFT JOIN students s ON gs.id = s.global_student_id
            WHERE gs.id = ?
        ''', (student_id,))
        return self.cursor.fetchone()

    def __del__(self):
        """Деструктор - закрываем соединение при удалении объекта."""
        self.disconnect()