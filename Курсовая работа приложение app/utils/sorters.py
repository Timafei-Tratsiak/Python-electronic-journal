"""
Сортировки
"""

def sort_by_marks(student_data):
    """Сортировать студентов по среднему баллу"""
    students_with_avg = []

    for student_id, data in student_data.items():
        avg_grade = calculate_average_grade(data)
        students_with_avg.append({
            'id': student_id,
            'data': data,
            'average': avg_grade
        })

    students_with_avg.sort(key=lambda x: x['average'], reverse=True)

    sorted_student_data = {}
    for idx, item in enumerate(students_with_avg):
        item['data']['row'] = idx + 1
        sorted_student_data[item['id']] = item['data']

    return sorted_student_data


def sort_by_alphabet(student_data):
    """Сортировать студентов по алфавиту"""
    students_list = []

    for student_id, data in student_data.items():
        students_list.append({
            'id': student_id,
            'data': data,
            'name': data['name']
        })

    students_list.sort(key=lambda x: x['name'])

    sorted_student_data = {}
    for idx, item in enumerate(students_list):
        item['data']['row'] = idx + 1
        sorted_student_data[item['id']] = item['data']

    return sorted_student_data


def calculate_average_grade(student_data):
    """Рассчитать средний балл студента"""
    grades = []

    for lesson_num, grade in student_data['grades'].items():
        if grade and grade.strip():
            try:
                grade_value = float(grade.strip())
                if 1 <= grade_value <= 10:
                    grades.append(grade_value)
            except ValueError:
                pass

    exam_grade = student_data['exam_grade']
    if exam_grade and exam_grade.strip():
        try:
            exam_grade_value = float(exam_grade.strip())
            if 1 <= exam_grade_value <= 10:
                grades.append(exam_grade_value)
        except ValueError:
            pass

    return sum(grades) / len(grades) if grades else -1