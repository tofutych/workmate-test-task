from unittest.mock import mock_open, patch

import pytest

from reporting import CsvReader

MOCK_CSV_FILE_CONTENT = """id,email,name,department,hours_worked,hourly_rate
1,alice@example.com,Alice Johnson,Marketing,160,50
2,bob@example.com,Bob Smith,Design,150,40
"""
MOCK_CSV_FILE_PATH = "./res/mock.csv"


@patch("builtins.open", new_callable=mock_open, read_data=MOCK_CSV_FILE_CONTENT)
def test_csv_reader(mock_file):
    reader = CsvReader("mock.csv")

    with reader:
        rows = reader.read()

    expected_header = [
        "id",
        "email",
        "name",
        "department",
        "hours",
        "rate",
    ]
    assert reader.get_header() == expected_header

    expected_rows = [
        {
            "id": "1",
            "email": "alice@example.com",
            "name": "Alice Johnson",
            "department": "Marketing",
            "hours": "160",
            "rate": "50",
        },
        {
            "id": "2",
            "email": "bob@example.com",
            "name": "Bob Smith",
            "department": "Design",
            "hours": "150",
            "rate": "40",
        },
    ]
    assert rows == expected_rows
    mock_file.assert_called_once_with(MOCK_CSV_FILE_PATH, "r", encoding="utf-8")


def test_csv_reader_file_not_found():
    non_existent_file = "non_existent_file.csv"
    with pytest.raises(FileNotFoundError, match=f"{non_existent_file} не найден!"):
        with CsvReader(non_existent_file) as reader:
            reader.read()


def test_csv_reader_outside_context_manager():
    reader = CsvReader("data1.csv")
    with pytest.raises(RuntimeError, match="Файл не открыт"):
        reader.read()


@patch("builtins.open", new_callable=mock_open, read_data="")
def test_csv_reader_empty_file(mock_file):
    with CsvReader("empty.csv") as reader:
        rows = reader.read()
        assert rows == []
        assert reader.get_header() == []


@patch("builtins.open", new_callable=mock_open, read_data="id,name")
def test_csv_reader_with_only_header(mock_file_open):
    with CsvReader("header_only.csv") as reader:
        rows = reader.read()

    assert rows == []
    assert reader.get_header() == ["id", "name"]
