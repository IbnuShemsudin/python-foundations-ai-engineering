
import csv
import json
import logging

from pathlib import Path

from src.models.student import Student
from src.utils.exceptions import StorageError


logger = logging.getLogger(__name__)


class FileStorage:

    def __init__(self, data_directory: str = "data"):
        self.data_directory = Path(data_directory)

        self.data_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        self.json_file = self.data_directory / "students.json"
        self.csv_file = self.data_directory / "students.csv"

    def load_students(self) -> list[Student]:

        if not self.json_file.exists():
            return []

        try:
            with open(
                self.json_file,
                "r",
                encoding="utf-8"
            ) as file:

                records = json.load(file)

            if not isinstance(records, list):
                raise ValueError("Student data must be a JSON list.")

            return [
                Student.from_dict(record)
                for record in records
            ]

        except (OSError, json.JSONDecodeError, ValueError, KeyError, TypeError) as error:
            logger.exception("Unable to load student records.")
            raise StorageError(
                "Could not load student records."
            ) from error

    def save_students(self, students: list[Student]) -> None:

        try:
            records = [
                student.to_dict()
                for student in students
            ]

            with open(
                self.json_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    records,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            logger.info("Student records saved successfully.")

        except (OSError, TypeError, ValueError) as error:
            logger.exception("Unable to save student records.")
            raise StorageError(
                "Could not save student records."
            ) from error

    def export_csv(self, students: list[Student]) -> None:

        fieldnames = [
            "student_id",
            "name",
            "age",
            "department",
            "score"
        ]

        try:
            with open(
                self.csv_file,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.DictWriter(
                    file,
                    fieldnames=fieldnames
                )

                writer.writeheader()

                for student in students:
                    writer.writerow(student.to_dict())

            logger.info("CSV export completed.")

        except OSError as error:
            logger.exception("CSV export failed.")
            raise StorageError(
                "Could not export student records."
            ) from error
