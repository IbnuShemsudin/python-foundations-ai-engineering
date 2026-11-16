
def validate_student_id(student_id: str) -> str:
    student_id = student_id.strip()

    if not student_id:
        raise ValueError("Student ID is required.")

    return student_id


def validate_name(name: str) -> str:
    name = name.strip()

    if len(name) < 2:
        raise ValueError("Name must contain at least 2 characters.")

    return name


def validate_age(age: int) -> int:
    if age <= 0:
        raise ValueError("Age must be greater than zero.")

    if age > 120:
        raise ValueError("Please enter a realistic age.")

    return age


def validate_score(score: float) -> float:
    if not 0 <= score <= 100:
        raise ValueError("Score must be between 0 and 100.")

    return score


def validate_department(department: str) -> str:
    department = department.strip()

    if not department:
        raise ValueError("Department is required.")

    return department
