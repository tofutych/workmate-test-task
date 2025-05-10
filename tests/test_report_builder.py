import pytest

from reporting import (
    BuilderFactory,
    DepartmentReport,
)


@pytest.fixture
def payout_builder():
    return BuilderFactory.get_builder(report_type="payout")


VALID_DATA = [
    {
        "id": "1",
        "name": "Alice",
        "email": "alice@example.com",
        "department": "Design",
        "hours": "160",
        "rate": "50",
    },
    {
        "id": "2",
        "name": "Alice",
        "email": "alice@example.com",
        "department": "Design",
        "hours": "150",
        "rate": "40",
    },
    {
        "id": "3",
        "name": "Bob",
        "email": "bob@example.com",
        "department": "HR",
        "hours": "170",
        "rate": "30",
    },
    {
        "id": "4",
        "name": "Charlie",
        "email": "charlie@example.com",
        "department": "Design",
        "hours": "100",
        "rate": "55",
    },
]
INVALID_DATA = [
    {
        "id": "1",
        "name": "Alice",
        "email": "alice@example.com",
        "department": "Design",
        "hours": "160",
        "rate": "50",
    },
    {
        "id": "2",
        "name": "Bob",
        "email": "bob@example.com",
        "department": "HR",
        "hours": "150",
        "rate": "bug",
    },
    {
        "id": "3",
        "name": "Charlie",
        "email": "charlie@example.com",
        "department": "HR",
        "hours": "100",
        "rate": "30",
    },
]


def test_payout_report_builder_valid_data(payout_builder):
    report = payout_builder.build_report(data=VALID_DATA)

    assert "Design" in report
    design_dept_report = report["Design"]
    assert isinstance(design_dept_report, DepartmentReport)

    expected_design_hours = 160 + 150 + 100
    expected_design_payout = (160 * 50) + (150 * 40) + (100 * 55)
    assert design_dept_report.department_total_hours == expected_design_hours
    assert design_dept_report.department_total_payout == expected_design_payout

    design_employee_names = {emp.name for emp in design_dept_report.employees}
    assert "Alice" in design_employee_names
    assert "Charlie" in design_employee_names
    assert len(design_dept_report.employees) == 3

    assert "HR" in report
    hr_dept_report = report["HR"]
    assert isinstance(hr_dept_report, DepartmentReport)
    assert hr_dept_report.department_total_hours == 170
    assert hr_dept_report.department_total_payout == (170 * 30)
    hr_employee_names = {emp.name for emp in hr_dept_report.employees}
    assert "Bob" in hr_employee_names
    assert len(hr_dept_report.employees) == 1


def test_payout_report_builder_invalid_data(payout_builder):
    report = payout_builder.build_report(data=INVALID_DATA)

    assert "HR" in report
    hr_dept_report = report["HR"]

    assert hr_dept_report.department_total_hours == 250
    assert hr_dept_report.department_total_payout == (100 * 30)

    hr_employee_names = {emp.name for emp in hr_dept_report.employees}
    assert "Charlie" in hr_employee_names


def test_builder_factory_get_builder_invalid_type():
    with pytest.raises(ValueError, match="Неподдерживаемый формат"):
        BuilderFactory.get_builder(report_type="unknown_report_type")
