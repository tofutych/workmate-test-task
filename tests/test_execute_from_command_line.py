from unittest.mock import MagicMock, patch

from services import execute_from_command_line

MOCK_PARSED_ARGS = {"files": ["file1.csv"], "report": "payout"}
MOCK_CSV_ROWS_DATA = [{"name": "Alice", "hours": "160", "rate": "50", "payout": "8000"}]
MOCK_BUILT_REPORT = {"Marketing_Department": "some_aggregated_report_data"}
MOCK_SERIALIZED_DATA = {"Marketing_Department": {"serialized_key": "serialized_value"}}


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
    mock_parse_args.return_value = MOCK_PARSED_ARGS

    mock_reader_instance = MagicMock()
    mock_reader_instance.read.return_value = MOCK_CSV_ROWS_DATA

    mock_csv_reader_class.return_value.__enter__.return_value = mock_reader_instance

    mock_builder_instance = MagicMock()
    mock_builder_instance.build_report.return_value = MOCK_BUILT_REPORT
    mock_get_builder.return_value = mock_builder_instance

    mock_serialize_report.return_value = MOCK_SERIALIZED_DATA

    mock_writer_instance = MagicMock()
    mock_get_writer.return_value = mock_writer_instance

    execute_from_command_line()

    mock_parse_args.assert_called_once_with()

    mock_csv_reader_class.assert_called_once_with(MOCK_PARSED_ARGS["files"][0])
    mock_reader_instance.read.assert_called_once_with()

    mock_get_builder.assert_called_once_with(report_type=MOCK_PARSED_ARGS["report"])
    mock_builder_instance.build_report.assert_called_once_with(data=MOCK_CSV_ROWS_DATA)

    mock_serialize_report.assert_called_once_with(MOCK_BUILT_REPORT)

    mock_writer_instance.write.assert_called_once_with(
        MOCK_SERIALIZED_DATA, f"{MOCK_PARSED_ARGS['report']}.json"
    )
