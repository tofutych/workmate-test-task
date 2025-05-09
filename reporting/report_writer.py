import json
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import override


class ReportWriter(ABC):
    @abstractmethod
    def write(self, data: defaultdict[str, list[dict[str, str]]], output_file: str):
        pass


class JSONReportWriter(ReportWriter):
    @override
    def write(
        self, data: defaultdict[str, list[dict[str, str]]], output_file: str
    ) -> None:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


class WriterFactory(object):
    writers: dict[str, type[ReportWriter]] = {
        "json": JSONReportWriter,
        # "excel": ExcelReportWriter,
        # "txt": TxtReportWriter,
    }

    @staticmethod
    def get_writer(extension_type: str = "json") -> ReportWriter:
        writer_class = WriterFactory.writers.get(extension_type.lower())
        if not writer_class:
            raise ValueError(f"Неподдерживаемый формат: {extension_type=}")
        return writer_class()
