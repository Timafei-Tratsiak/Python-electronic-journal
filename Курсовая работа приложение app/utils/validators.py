"""
Валидаторы для ввода данных
"""

def validate_integer_input(value, min_val=1, max_val=100):
    """Валидация целого числа"""
    if value == "":
        return True
    if value.isdigit():
        num = int(value)
        return min_val <= num <= max_val
    return False


def validate_subject_name(value, max_length=100):
    """Валидация названия предмета"""
    if value is None:
        return False
    return len(value) <= max_length


def validate_grade(value, min_grade=1, max_grade=10):
    """Валидация оценки"""
    if value == "" or value is None:
        return True
    try:
        grade = float(value)
        return min_grade <= grade <= max_grade
    except (ValueError, TypeError):
        return False


def validate_grade_input(P):
    """Валидация оценки для использования в Entry"""
    return validate_grade(P)