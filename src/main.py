
import logging

from pathlib import Path

from src.storage.file_storage import FileStorage
from src.services.student_service import StudentService
from src.reports.report_generator import ReportGenerator

from src.utils.exceptions import (
    DuplicateStudentError,
    StudentNotFoundError,
    StorageError
)


# Create application directories.
Path("logs").mkdir(exist_ok=True)

# Configure logging.
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)


def get_integer(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))

        except ValueError:
            print("Please enter a valid whole number.")


def get_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))

        except ValueError:
            print("Please enter a valid number.")


def display_menu() -> None:
    print("\n" + "=" * 45)
    print("       STUDENT RECORDS MANAGEMENT")
    print("=" * 45)

    print("1. Add student")
    print("2. View all students")
    print("3. Find student")
    print("4. Update student")
    print("5. Delete student")
    print("6. Academic statistics")
    print("7. Export CSV")
    print("8. Generate academic report")
    print("0. Exit")

    print("=" * 45)


def add_student(service: StudentService) -> None:

    print("\n--- Add Student ---")

    student = service.add_student(
        student_id=input("Student ID: "),
        name=input("Student name: "),
        age=get_integer("Age: "),
        department=input("Department: "),
        score=get_float("Score: ")
    )

    print(f"Student {student.name} added successfully.")


def view_students(service: StudentService) -> None:

    students = service.get_all_students()

    if not students:
        print("No students registered yet.")
        return

    print("\n--- Student Records ---")

    for student in students:
        print("-" * 40)

        print("ID:", student.student_id)
        print("Name:", student.name)
        print("Age:", student.age)
        print("Department:", student.department)
        print("Score:", student.score)
        print("Grade:", student.get_grade())
        print("Result:", "Passed" if student.is_passed() else "Failed")


def find_student(service: StudentService) -> None:

    student_id = input("Enter student ID: ")

    student = service.find_student(student_id)

    print("\nStudent found:")
    print(student)


def update_student(service: StudentService) -> None:

    student_id = input("Enter student ID: ")

    student = service.find_student(student_id)

    print("Leave a field empty to keep its current value.")

    name = input(f"Name [{student.name}]: ").strip()
    age_input = input(f"Age [{student.age}]: ").strip()
    department = input(
        f"Department [{student.department}]: "
    ).strip()
    score_input = input(f"Score [{student.score}]: ").strip()

    updated_student = service.update_student(
        student_id=student_id,
        name=name if name else None,
        age=int(age_input) if age_input else None,
        department=department if department else None,
        score=float(score_input) if score_input else None
    )

    print("Student updated successfully.")
    print(updated_student)


def delete_student(service: StudentService) -> None:

    student_id = input("Enter student ID: ")

    student = service.find_student(student_id)

    confirmation = input(
        f"Delete {student.name}? (y/n): "
    ).strip().lower()

    if confirmation == "y":
        service.delete_student(student_id)
        print("Student deleted successfully.")
    else:
        print("Deletion cancelled.")


def display_statistics(service: StudentService) -> None:

    students = service.get_all_students()

    if not students:
        print("No student records available.")
        return

    highest = service.get_highest_performer()
    lowest = service.get_lowest_performer()

    print("\n--- Academic Statistics ---")

    print("Total students:", len(students))
    print("Average score:", round(service.get_average_score(), 2))
    print("Passed:", service.get_passed_count())
    print("Failed:", service.get_failed_count())

    print(
        "Highest performer:",
        highest.name,
        highest.score
    )

    print(
        "Lowest performer:",
        lowest.name,
        lowest.score
    )


def run_application() -> None:

    storage = FileStorage("data")
    service = StudentService(storage)

    report_generator = ReportGenerator("data/reports")

    logger.info("Student management application started.")

    while True:

        display_menu()

        choice = input("Choose an option: ").strip()

        try:

            if choice == "1":
                add_student(service)

            elif choice == "2":
                view_students(service)

            elif choice == "3":
                find_student(service)

            elif choice == "4":
                update_student(service)

            elif choice == "5":
                delete_student(service)

            elif choice == "6":
                display_statistics(service)

            elif choice == "7":
                service.export_students()
                print("CSV export completed.")

            elif choice == "8":
                report_generator.generate_report(
                    service.get_all_students()
                )

            elif choice == "0":
                print("Thank you for using the application.")

                logger.info("Application closed.")

                break

            else:
                print("Invalid option. Please try again.")

        except (
            ValueError,
            DuplicateStudentError,
            StudentNotFoundError,
            StorageError
        ) as error:

            print("Operation failed:", error)
            logger.warning("Operation failed: %s", error)

        except (OSError, TypeError) as error:

            print("Unexpected operation error:", error)
            logger.exception("Unexpected application error.")


if __name__ == "__main__":

    try:
        run_application()

    except StorageError as error:
        print("Application could not start:", error)
        logger.exception("Application startup failed.")
