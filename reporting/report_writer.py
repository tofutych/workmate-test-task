import json
from abc import ABC, abstractmethod
from typing import override


class ReportWriter(ABC):
    @abstractmethod
    def write(self, data: dict[str, dict[str, str | int]], output_file: str):
        pass


class JSONReportWriter(ReportWriter):
    @override
    def write(self, data: dict[str, dict[str, str | int]], output_file: str) -> None:
        with open(f"{output_file}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


class WriterFactory(object):
    writers: dict[str, type[ReportWriter]] = {
        "json": JSONReportWriter,
        # "excel": ExcelReportWriter,
        # "txt": TxtReportWriter,
    }

    @classmethod
    def get_writer(cls, extension_type: str = "json") -> ReportWriter:
        writer_class = WriterFactory.writers.get(extension_type.lower())
        if not writer_class:
            raise ValueError(f"Неподдерживаемый формат: {extension_type=}")
        return writer_class()
