from abc import ABC, abstractmethod
from collections import defaultdict
from typing import override


class ReportBuilder(ABC):
    @abstractmethod
    def build_report(self, data: list[dict[str, str]]) -> list[list[str]]:
        pass

    @staticmethod
    def str_to_int(value: str | None, default: int = 0) -> int:
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def group_by_department(data):
        pass


class PayoutBuilder(ReportBuilder):
    @override
    def build_report(self, data: list[dict[str, str]]):
        departments = {}
        template_keys = ["id", "name", "hours", "rate", "payout"]
        result: list[list[str]] = []
        grouped: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
        for item in data:
            hours = self.__class__.str_to_int(item["hours"])
            rate = self.__class__.str_to_int(item.get("rate"))
            employee_payout = hours * rate
            item["payout"] = f"{employee_payout}"

            if item["department"] not in departments.keys():
                departments[f"{item['department']}"] = 0
            departments[f"{item['department']}"] += employee_payout

            department = item.get("department", "Unknown")
            item.pop("email")  # pyright: ignore[reportUnusedCallResult]
            item.pop("department")  # pyright: ignore[reportUnusedCallResult]
            if not result:
                result.append(list(item.keys()))
                result[0][0] = ""
            normalized_employee = {key: item.get(key, "") for key in template_keys}
            grouped[department].append(normalized_employee)

        for department, employees in grouped.items():
            result.append([department, "", "", "", ""])
            department_total_hours = 0
            department_total_payout = 0
            for employee in employees:
                department_total_hours += self.__class__.str_to_int(employee["hours"])
                department_total_payout += self.__class__.str_to_int(employee["payout"])
                employee["id"] = "--------------"
                employee["payout"] = f"${employee['payout']}"
                result.append(list((employee.values())))

            result.append(
                [
                    "",
                    "",
                    str(department_total_hours),
                    "",
                    f"${department_total_payout}",
                ]
            )
        return result


class BuilderFactory(object):
    builders: dict[str, type[ReportBuilder]] = {
        "payout": PayoutBuilder,
        # "excel": ExcelReportWriter,
        # "txt": TxtReportWriter,
    }

    @staticmethod
    def get_builder(report_type: str = "payout") -> ReportBuilder:
        builder_class = BuilderFactory.builders.get(report_type.lower())
        if not builder_class:
            raise ValueError(f"Неподдерживаемый формат: {report_type=}")
        return builder_class()
