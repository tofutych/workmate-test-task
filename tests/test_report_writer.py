import json
from unittest.mock import mock_open, patch

import pytest

from reporting.report_writer import JSONReportWriter, WriterFactory


def test_get_writer_valid():
    writer = WriterFactory.get_writer("json")
    assert isinstance(writer, JSONReportWriter)


def test_get_writer_invalid():
    with pytest.raises(ValueError, match="Неподдерживаемый формат"):
        WriterFactory.get_writer("txt")


@patch("builtins.open", new_callable=mock_open)
def test_write_json_report(mock_file):
    data = {
        "Marketing": {
            "employees": [
                {
                    "name": "Alice Johnson",
                    "hours": "160",
                    "rate": "50",
                    "payout": "8000",
                },
                {
                    "name": "Henry Martin",
                    "hours": "150",
                    "rate": "35",
                    "payout": "5250",
                },
            ],
            "department_total_payout": 13250,
            "department_total_hours": 310,
        }
    }

    writer = JSONReportWriter()
    writer.write(data, "payout")

    handle = mock_file()
    written_data = "".join(call.args[0] for call in handle.write.call_args_list)

    expected_data = json.dumps(data, indent=2)

    written_data = written_data.strip()
    expected_data = expected_data.strip()

    assert written_data == expected_data
