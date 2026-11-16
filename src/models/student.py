
from dataclasses import dataclass


@dataclass
class Student:
    student_id: str
    name: str
    age: int
    department: str
    score: float

    def __post_init__(self) -> None:
        self.student_id = self.student_id.strip()
        self.name = self.name.strip()
        self.department = self.department.strip()

        if not self.student_id:
            raise ValueError("Student ID cannot be empty.")

        if not self.name:
            raise ValueError("Student name cannot be empty.")

        if self.age <= 0:
            raise ValueError("Age must be greater than zero.")

        if not self.department:
            raise ValueError("Department cannot be empty.")

        if not 0 <= self.score <= 100:
            raise ValueError("Score must be between 0 and 100.")

    def get_grade(self) -> str:
        if self.score >= 90:
            return "A"
        elif self.score >= 80:
            return "B"
        elif self.score >= 70:
            return "C"
        elif self.score >= 60:
            return "D"
        return "F"

    def is_passed(self) -> bool:
        return self.score >= 50

    def update_score(self, new_score: float) -> None:
        if not 0 <= new_score <= 100:
            raise ValueError("Score must be between 0 and 100.")

        self.score = new_score

    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "department": self.department,
            "score": self.score
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        return cls(
            student_id=str(data["student_id"]),
            name=str(data["name"]),
            age=int(data["age"]),
            department=str(data["department"]),
            score=float(data["score"])
        )
