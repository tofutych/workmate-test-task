import json
from unittest.mock import mock_open, patch

import pytest

from reporting.report_writer import JSONReportWriter, WriterFactory

SAMPLE_REPORT_DATA = {
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


def test_writer_factory_get_writer_returns_json_writer():
    writer = WriterFactory.get_writer("json")
    assert isinstance(writer, JSONReportWriter)


def test_writer_factory_get_writer_invalid_type():
    with pytest.raises(ValueError, match="Неподдерживаемый формат"):
        WriterFactory.get_writer("unknown")


@patch("builtins.open", new_callable=mock_open)
def test_json_report_writer_writes_correct_json_content(mock_file_open):
    writer = JSONReportWriter()
    output_filename = "payout.json"

    writer.write(SAMPLE_REPORT_DATA, output_filename)

    mock_file_open.assert_called_once_with(output_filename, "w", encoding="utf-8")

    written_calls = mock_file_open().write.call_args_list
    written_content_actual = "".join(call.args[0] for call in written_calls)

    assert json.loads(written_content_actual) == SAMPLE_REPORT_DATA
