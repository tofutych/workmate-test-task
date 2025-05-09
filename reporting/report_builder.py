from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import override


@dataclass
class Employee:
    name: str
    hours: str
    rate: str | int
    payout: str | int


@dataclass
class DepartmentReport:
    employees: list[Employee] = field(default_factory=list)
    department_total_payout: int = 0
    department_total_hours: int = 0


class ReportBuilder(ABC):
    @abstractmethod
    def build_report(self, data: list[dict[str, str]]) -> dict[str, DepartmentReport]:
        pass

    @staticmethod
    def str_to_int(value: str | None, default: int = 0) -> int:
        try:
            return int(value) if value else default
        except (ValueError, TypeError):
            return default

    def _calculate_employee_payout(self, item: dict[str, str]) -> tuple[int, int]:
        hours = self.str_to_int(item.get("hours"))
        rate = self.str_to_int(item.get("rate"))
        payout = hours * rate
        return hours, payout

    def _normalize_employee(
        self, item: dict[str, str], template_keys: list[str]
    ) -> Employee:
        normalized = {key: item.get(key, "") for key in template_keys}
        return Employee(**normalized)


class PayoutBuilder(ReportBuilder):
    TEMPLATE_KEYS: list[str] = ["name", "hours", "rate", "payout"]

    @override
    def build_report(self, data: list[dict[str, str]]) -> dict[str, DepartmentReport]:
        seen_ids: set[str] = set()
        try:
            grouped: defaultdict[str, DepartmentReport] = defaultdict(
                lambda: DepartmentReport()
            )
            for row in data:
                hours, employee_payout = self._calculate_employee_payout(row)
                row["payout"] = f"{employee_payout}"

                if row["id"] in seen_ids:
                    print(f"⚠️ Пропущен сотрудник с дублирующимся id:\n{row}")
                    continue
                seen_ids.add(row["id"])

                department = row.get("department", "Unknown")
                grouped[department].department_total_hours += hours
                grouped[department].department_total_payout += employee_payout

                row.pop("email", None)  # pyright: ignore[reportUnusedCallResult]
                row.pop("department", None)  # pyright: ignore[reportUnusedCallResult]

                row = self._normalize_employee(row, self.TEMPLATE_KEYS)
                grouped[department].employees.append(row)
            return grouped
        except ValueError as e:
            raise ValueError(f"Неправильный формат данных: {e}") from None


class BuilderFactory(object):
    builders: dict[str, type[ReportBuilder]] = {
        "payout": PayoutBuilder,
        # "excel": ExcelReportWriter,
        # "txt": TxtReportWriter,
    }

    @classmethod
    def get_builder(cls, report_type: str = "payout") -> ReportBuilder:
        builder_class = BuilderFactory.builders.get(report_type.lower())
        if not builder_class:
            raise ValueError(f"Неподдерживаемый формат: {report_type=}")
        return builder_class()
