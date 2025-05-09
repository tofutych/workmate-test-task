import pytest

from reporting import BuilderFactory


def test_build_report_valid():
    data = [
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
            "hours": "150",
            "rate": "bug",
        },
        {
            "id": "3",
            "name": "Bob",
            "email": "bob@example.com",
            "department": "HR",
            "hours": "150",
            "rate": "bug",
        },
    ]

    builder = BuilderFactory.builders.get("payout")

    builder = BuilderFactory.get_builder(report_type="payout")

    report = builder.build_report(data=data)

    assert "Design" in report
    department = report["Design"]
    assert department.department_total_hours == 310
    assert department.department_total_payout == (160 * 50 + 150 * 40)

    employee_names = [emp.name for emp in department.employees]
    assert "Alice" in employee_names
    assert "Bob" not in employee_names


def test_get_builder_invalid_type():
    with pytest.raises(ValueError, match="Неподдерживаемый формат"):
        BuilderFactory.get_builder(report_type="unknown")
