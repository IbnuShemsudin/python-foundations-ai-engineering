
import tempfile
import unittest

from pathlib import Path

from src.models.student import Student
from src.storage.file_storage import FileStorage
from src.services.student_service import StudentService

from src.utils.exceptions import (
    DuplicateStudentError,
    StudentNotFoundError
)


class TestStudentModel(unittest.TestCase):

    def test_student_grade(self):
        student = Student(
            "ST001", "Abdurezak", 24,
            "Software Engineering", 95
        )

        self.assertEqual(student.get_grade(), "A")

    def test_student_passed(self):
        student = Student(
            "ST002", "Ahmed", 23,
            "Computer Science", 85
        )

        self.assertTrue(student.is_passed())

    def test_invalid_score(self):
        with self.assertRaises(ValueError):
            Student(
                "ST003", "Fatima", 22,
                "Software Engineering", 150
            )


class TestStudentService(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()

        self.storage = FileStorage(
            self.temp_directory.name
        )

        self.service = StudentService(self.storage)

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_add_student(self):

        student = self.service.add_student(
            "ST001",
            "Abdurezak",
            24,
            "Software Engineering",
            95
        )

        self.assertEqual(student.student_id, "ST001")
        self.assertEqual(len(self.service.get_all_students()), 1)

    def test_duplicate_student(self):

        self.service.add_student(
            "ST001",
            "Abdurezak",
            24,
            "Software Engineering",
            95
        )

        with self.assertRaises(DuplicateStudentError):
            self.service.add_student(
                "ST001",
                "Ahmed",
                23,
                "Computer Science",
                80
            )

    def test_find_missing_student(self):

        with self.assertRaises(StudentNotFoundError):
            self.service.find_student("ST999")

    def test_persistence(self):

        self.service.add_student(
            "ST001",
            "Abdurezak",
            24,
            "Software Engineering",
            95
        )

        # Create a new service using the same storage.
        new_service = StudentService(self.storage)

        self.assertEqual(
            len(new_service.get_all_students()),
            1
        )

        self.assertEqual(
            new_service.find_student("ST001").name,
            "Abdurezak"
        )

    def test_update_student(self):

        self.service.add_student(
            "ST001",
            "Abdurezak",
            24,
            "Software Engineering",
            95
        )

        updated = self.service.update_student(
            "ST001",
            score=98
        )

        self.assertEqual(updated.score, 98)

    def test_average_score(self):

        self.service.add_student(
            "ST001", "Abdurezak", 24,
            "Software Engineering", 90
        )

        self.service.add_student(
            "ST002", "Ahmed", 23,
            "Computer Science", 80
        )

        self.assertEqual(
            self.service.get_average_score(),
            85
        )


if __name__ == "__main__":
    unittest.main()
