import argparse
from typing import TypedDict, cast

from reporting import CsvReader, WriterFactory
from reporting.report_builder import BuilderFactory


class Args(TypedDict):
    files: list[str]
    report: str


def parse_args() -> Args:
    parser = argparse.ArgumentParser(description="Скрипт для создания отчетов")
    file_group = parser.add_argument_group("Файлы")
    file_group.add_argument("files", nargs="+", help="Список из путей к файлам")  # pyright: ignore[reportUnusedCallResult]
    report_group = parser.add_argument_group("Тип отчета")
    report_group.add_argument("--report", help="Вид отчета")  # pyright: ignore[reportUnusedCallResult]
    args: argparse.Namespace = parser.parse_args()
    return cast(Args, cast(object, vars(args)))


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
    writer = WriterFactory.get_writer(extension_type="json")
    writer.write(report_data, f"{report_type}.json")
