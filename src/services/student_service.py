
import logging

from src.models.student import Student
from src.storage.file_storage import FileStorage
from src.utils.exceptions import (
    DuplicateStudentError,
    StudentNotFoundError
)
from src.utils.validators import (
    validate_student_id,
    validate_name,
    validate_age,
    validate_score,
    validate_department
)


logger = logging.getLogger(__name__)


class StudentService:

    def __init__(self, storage: FileStorage):
        self.storage = storage
        self.students = self.storage.load_students()

    def add_student(
        self,
        student_id: str,
        name: str,
        age: int,
        department: str,
        score: float
    ) -> Student:

        student_id = validate_student_id(student_id)

        if self.find_student(student_id, raise_error=False):
            raise DuplicateStudentError(
                f"Student {student_id} already exists."
            )

        student = Student(
            student_id=student_id,
            name=validate_name(name),
            age=validate_age(age),
            department=validate_department(department),
            score=validate_score(score)
        )

        self.students.append(student)
        self.storage.save_students(self.students)

        logger.info("Student added: %s", student_id)

        return student

    def get_all_students(self) -> list[Student]:
        return self.students.copy()

    def find_student(
        self,
        student_id: str,
        raise_error: bool = True
    ) -> Student | None:

        student_id = validate_student_id(student_id)

        for student in self.students:
            if student.student_id == student_id:
                return student

        if raise_error:
            raise StudentNotFoundError(
                f"Student {student_id} was not found."
            )

        return None

   
def update_student(
    self,
    student_id: str,
    name: str | None = None,
    age: int | None = None,
    department: str | None = None,
    score: float | None = None
) -> Student:

    student = self.find_student(student_id)

    # Validate everything before modifying the student.
    new_name = (
        validate_name(name)
        if name is not None
        else student.name
    )

    new_age = (
        validate_age(age)
        if age is not None
        else student.age
    )

    new_department = (
        validate_department(department)
        if department is not None
        else student.department
    )

    new_score = (
        validate_score(score)
        if score is not None
        else student.score
    )

    student.name = new_name
    student.age = new_age
    student.department = new_department
    student.score = new_score

    self.storage.save_students(self.students)

    logger.info("Student updated: %s", student_id)

    return student


    def delete_student(self, student_id: str) -> None:

        student = self.find_student(student_id)

        self.students.remove(student)

        self.storage.save_students(self.students)

        logger.info("Student deleted: %s", student_id)

    def export_students(self) -> None:
        self.storage.export_csv(self.students)

    def get_average_score(self) -> float:

        if not self.students:
            return 0.0

        return sum(
            student.score for student in self.students
        ) / len(self.students)

    def get_highest_performer(self) -> Student | None:

        if not self.students:
            return None

        return max(
            self.students,
            key=lambda student: student.score
        )

    def get_lowest_performer(self) -> Student | None:

        if not self.students:
            return None

        return min(
            self.students,
            key=lambda student: student.score
        )

    def get_passed_count(self) -> int:
        return sum(
            student.is_passed()
            for student in self.students
        )

    def get_failed_count(self) -> int:
        return sum(
            not student.is_passed()
            for student in self.students
        )
