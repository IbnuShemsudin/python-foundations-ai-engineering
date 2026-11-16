
import logging
from pathlib import Path

import pandas as pd

from src.models.student import Student


logger = logging.getLogger(__name__)


class ReportGenerator:

    def __init__(self, output_directory: str = "data/reports"):
        self.output_directory = Path(output_directory)

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

    def generate_report(
        self,
        students: list[Student]
    ) -> None:

        if not students:
            print("No student records available for reporting.")
            return

        records = [
            student.to_dict()
            for student in students
        ]

        df = pd.DataFrame(records)

        df["score"] = pd.to_numeric(
            df["score"],
            errors="raise"
        )

        print("\n========== ACADEMIC REPORT ==========")

        print("Total students:", len(df))
        print("Average score:", round(df["score"].mean(), 2))
        print("Highest score:", df["score"].max())
        print("Lowest score:", df["score"].min())

        passed = int((df["score"] >= 50).sum())
        failed = int((df["score"] < 50).sum())

        print("Passed:", passed)
        print("Failed:", failed)

        print("\nDepartment performance:")

        department_report = (
            df.groupby("department")["score"]
            .mean()
            .round(2)
        )

        print(department_report)

        report_file = (
            self.output_directory / "academic_report.csv"
        )

        df.to_csv(report_file, index=False)

        logger.info("Academic report generated.")

        print("\nReport saved to:", report_file)
