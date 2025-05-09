from unittest.mock import mock_open, patch

import pytest

from reporting import CsvReader

MOCK_FILE_CONTENT = """id,email,name,department,hours_worked,hourly_rate
1,alice@example.com,Alice Johnson,Marketing,160,50
2,bob@example.com,Bob Smith,Design,150,40
"""


@patch("builtins.open", new_callable=mock_open, read_data=MOCK_FILE_CONTENT)
def test_csv_reader(mock_file):
    reader = CsvReader("mock.csv")
    with reader:
        rows = reader.read()
    assert reader.get_header() == [
        "id",
        "email",
        "name",
        "department",
        "hours",
        "rate",
    ]
    assert rows == [
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
    mock_file.assert_called_once_with("./res/mock.csv", "r", encoding="utf-8")


def test_csv_reader_file_not_found():
    with pytest.raises(FileNotFoundError, match="delete_me.csv не найден!"):
        with CsvReader("delete_me.csv") as reader:
            reader.read()


def test_read_without_context_manager_raises():
    reader = CsvReader("data1.csv")

    with pytest.raises(RuntimeError, match="Файл не открыт"):
        reader.read()


@patch("builtins.open", new_callable=mock_open, read_data="")
def test_csv_reader_empty_file(mock_file):
    with CsvReader("empty.csv") as reader:
        result = reader.read()
        assert result == []
        assert reader.get_header() == []
