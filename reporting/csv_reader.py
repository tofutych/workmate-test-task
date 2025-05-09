from typing import TextIO


class CsvReader:
    def __init__(self, filepath: str) -> None:
        self.filepath: str = filepath
        self.header: list[str] = []
        self.rows: list[dict[str, str]] = []
        self._file: TextIO | None

    def __enter__(self) -> "CsvReader":
        try:
            self._file = open(f"./res/{self.filepath}", "r", encoding="utf-8")
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self.filepath} не найден!") from None
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._file:
            self._file.close()

    def _parse_line(self, line: str, delimiter: str = ",") -> list[str]:
        return [value.strip() for value in line.split(delimiter)]

    def _header_normalization(self, header: list[str]):
        COLUMN_NAME_ALIASES = {
            "id": [
                "id",
            ],
            "email": [
                "email",
            ],
            "name": [
                "name",
            ],
            "department": [
                "department",
            ],
            "hours": [
                "hours",
                "hours_worked",
                "worked_hours",
            ],
            "rate": [
                "rate",
                "salary",
                "hourly_rate",
            ],
        }
        header = [h.lower().strip() for h in header]
        for name, aliases in COLUMN_NAME_ALIASES.items():
            for alias in aliases:
                if alias in header:
                    header[header.index(alias)] = name
        return header

    def _to_dict(self, values: list[str]) -> dict[str, str]:
        return dict(zip(self.header, values))

    def read(self) -> list[dict[str, str]]:
        if not self._file:
            raise RuntimeError("Файл не открыт. Используйте контекстный менеджер.")

        lines = self._file.read().splitlines()

        if not lines:
            return []

        self.header = self._header_normalization(self._parse_line(lines[0]))
        self.rows = [self._to_dict(self._parse_line(line)) for line in lines[1:]]

        return self.rows

    def get_header(self) -> list[str]:
        return self.header

    def get_rows(self) -> list[dict[str, str]]:
        return self.rows
