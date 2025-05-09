from unittest.mock import MagicMock, patch

from services import execute_from_command_line


@patch("services.WriterFactory.get_writer")
@patch("services.serialize_report")
@patch("services.BuilderFactory.get_builder")
@patch("services.CsvReader")
@patch("services.parse_args")
def test_execute_from_command_line(
    mock_parse_args,
    mock_csv_reader_class,
    mock_get_builder,
    mock_serialize_report,
    mock_get_writer,
):
    mock_parse_args.return_value = {
        "files": ["file1.csv"],
        "report": "payout",
    }

    mock_reader = MagicMock()
    mock_reader.read.return_value = [
        {"name": "Alice", "hours": "160", "rate": "50", "payout": "8000"}
    ]
    mock_csv_reader_class.return_value.__enter__.return_value = mock_reader

    mock_builder = MagicMock()
    mock_builder.build_report.return_value = {"Marketing": "some_report"}
    mock_get_builder.return_value = mock_builder

    mock_serialize_report.return_value = {"Marketing": {"...": "..."}}

    mock_writer = MagicMock()
    mock_get_writer.return_value = mock_writer

    execute_from_command_line()

    mock_parse_args.assert_called_once()
    mock_csv_reader_class.assert_called_once_with("file1.csv")
    mock_reader.read.assert_called_once()
    mock_get_builder.assert_called_once_with(report_type="payout")
    mock_builder.build_report.assert_called_once_with(
        data=[{"name": "Alice", "hours": "160", "rate": "50", "payout": "8000"}]
    )
    mock_serialize_report.assert_called_once_with({"Marketing": "some_report"})
    mock_writer.write.assert_called_once_with({"Marketing": {"...": "..."}}, "payout")
