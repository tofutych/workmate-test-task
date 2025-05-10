import pytest

from reporting import DepartmentReport, Employee
from services import serialize_report

SERIALIZATION_TEST_CASES = [
    (
        "single_department_single_employee",
        {
            "Marketing": DepartmentReport(
                employees=[
                    Employee(
                        name="Alice Johnson", hours="160", rate="50", payout="8000"
                    )
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
                    }
                ],
                "department_total_payout": 8000,
                "department_total_hours": 160,
            }
        },
    ),
    (
        "multiple_departments_multiple_employees",
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
                        name="Carol Williams", hours="170", rate="60", payout="10200"
                    )
                ],
                department_total_payout=10200,
                department_total_hours=170,
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
        },
    ),
    (
        "department_with_no_employees",
        {
            "Legal": DepartmentReport(
                employees=[], department_total_payout=0, department_total_hours=0
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
        "department_with_zero_value_employee",
        {
            "Support": DepartmentReport(
                employees=[Employee(name="John Zero", hours="0", rate="0", payout="0")],
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
    ("empty_input_report_data", {}, {}),
]


@pytest.mark.parametrize(
    "test_id, input_report_objects, expected_serialized_dict",
    SERIALIZATION_TEST_CASES,
    ids=[case[0] for case in SERIALIZATION_TEST_CASES],
)
def test_serialize_report_converts_report_objects_to_dictionaries(
    test_id, input_report_objects, expected_serialized_dict
):
    assert serialize_report(input_report_objects) == expected_serialized_dict
