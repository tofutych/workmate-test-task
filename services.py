import argparse
from dataclasses import asdict
from typing import TypedDict, cast

from reporting import BuilderFactory, CsvReader, DepartmentReport, WriterFactory


class CliArgs(TypedDict):
    files: list[str]
    report: str


def parse_args() -> CliArgs:
    parser = argparse.ArgumentParser(description="Скрипт для создания отчетов")

    file_group = parser.add_argument_group("Файлы")
    file_group.add_argument("files", nargs="+", help="Список из путей к файлам")  # pyright: ignore[reportUnusedCallResult]

    report_group = parser.add_argument_group("Тип отчета")
    report_group.add_argument("--report", type=str, required=True, help="Вид отчета")  # pyright: ignore[reportUnusedCallResult]
    args: argparse.Namespace = parser.parse_args()
    return cast(CliArgs, cast(object, vars(args)))


def serialize_report(
    report: dict[str, DepartmentReport],
) -> dict[str, dict[str, str | int]]:
    return {department: asdict(data) for department, data in report.items()}


def execute_from_command_line():
    args = parse_args()
    files = args["files"]
    report_type = args["report"]

    data: list[dict[str, str]] = []
    for file_path in files:
        with CsvReader(file_path) as reader:
            rows = reader.read()
            for row in rows:
                data.append(row)

    builder = BuilderFactory.get_builder(report_type=report_type)
    report_data = builder.build_report(data=data)
    serialized_report_data = serialize_report(report_data)
    writer = WriterFactory.get_writer(extension_type="json")
    writer.write(serialized_report_data, report_type)
