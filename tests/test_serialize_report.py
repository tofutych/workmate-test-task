import pytest

from reporting import DepartmentReport, Employee
from services import serialize_report


@pytest.mark.parametrize(
    "input_data,expected_output",
    [
        (
            {
                "Marketing": DepartmentReport(
                    employees=[
                        Employee(
                            name="Alice Johnson", hours="160", rate="50", payout="8000"
                        ),
                    ],
                    department_total_payout=8000,
                    department_total_hours=160,
                )
            },
            {
                "Marketing": {
                    "employees": [
                        {
                            "name": "Alice Johnson",
                            "hours": "160",
                            "rate": "50",
                            "payout": "8000",
                        },
                    ],
                    "department_total_payout": 8000,
                    "department_total_hours": 160,
                }
            },
        ),
        (
            {
                "Marketing": DepartmentReport(
                    employees=[
                        Employee(
                            name="Alice Johnson", hours="160", rate="50", payout="8000"
                        ),
                        Employee(
                            name="Henry Martin", hours="150", rate="35", payout="5250"
                        ),
                    ],
                    department_total_payout=13250,
                    department_total_hours=310,
                ),
                "Design": DepartmentReport(
                    employees=[
                        Employee(
                            name="Carol Williams",
                            hours="170",
                            rate="60",
                            payout="10200",
                        ),
                    ],
                    department_total_payout=10200,
                    department_total_hours=170,
                ),
                "HR": DepartmentReport(
                    employees=[
                        Employee(
                            name="Liam Harris", hours="155", rate="42", payout="6510"
                        ),
                    ],
                    department_total_payout=6510,
                    department_total_hours=42,
                ),
            },
            {
                "Marketing": {
                    "employees": [
                        {
                            "name": "Alice Johnson",
                            "hours": "160",
                            "rate": "50",
                            "payout": "8000",
                        },
                        {
                            "name": "Henry Martin",
                            "hours": "150",
                            "rate": "35",
                            "payout": "5250",
                        },
                    ],
                    "department_total_payout": 13250,
                    "department_total_hours": 310,
                },
                "Design": {
                    "employees": [
                        {
                            "name": "Carol Williams",
                            "hours": "170",
                            "rate": "60",
                            "payout": "10200",
                        }
                    ],
                    "department_total_payout": 10200,
                    "department_total_hours": 170,
                },
                "HR": {
                    "employees": [
                        {
                            "name": "Liam Harris",
                            "hours": "155",
                            "rate": "42",
                            "payout": "6510",
                        }
                    ],
                    "department_total_payout": 6510,
                    "department_total_hours": 42,
                },
            },
        ),
        (
            {
                "Legal": DepartmentReport(
                    employees=[],
                    department_total_payout=0,
                    department_total_hours=0,
                )
            },
            {
                "Legal": {
                    "employees": [],
                    "department_total_payout": 0,
                    "department_total_hours": 0,
                }
            },
        ),
        (
            {
                "Support": DepartmentReport(
                    employees=[
                        Employee(name="John Zero", hours="0", rate="0", payout="0"),
                    ],
                    department_total_payout=0,
                    department_total_hours=0,
                )
            },
            {
                "Support": {
                    "employees": [
                        {"name": "John Zero", "hours": "0", "rate": "0", "payout": "0"}
                    ],
                    "department_total_payout": 0,
                    "department_total_hours": 0,
                }
            },
        ),
        ({}, {}),
    ],
)
def test_serialize_report(input_data, expected_output):
    assert serialize_report(input_data) == expected_output
