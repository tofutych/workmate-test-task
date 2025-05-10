import sys

import pytest

from services import parse_args


def test_parse_args_valid(monkeypatch):
    test_argv = ["script_name.py", "file1.csv", "file2.csv", "--report", "payout"]
    monkeypatch.setattr(sys, "argv", test_argv)

    expected_result = {
        "files": ["file1.csv", "file2.csv"],
        "report": "payout",
    }
    assert parse_args() == expected_result


def test_parse_args_missing_report_argument(monkeypatch):
    test_argv = ["script_name.py", "file1.csv"]
    monkeypatch.setattr(sys, "argv", test_argv)

    with pytest.raises(SystemExit):
        parse_args()


def test_parse_args_missing_file_arguments(monkeypatch):
    test_argv = ["script_name.py", "--report", "payout"]
    monkeypatch.setattr(sys, "argv", test_argv)

    with pytest.raises(SystemExit):
        parse_args()


def test_parse_args_unknown_report_type(monkeypatch):
    test_argv = ["script_name.py", "file1.csv", "--report", "unknown"]
    monkeypatch.setattr(sys, "argv", test_argv)

    expected_result = {
        "files": ["file1.csv"],
        "report": "unknown",
    }
    assert parse_args() == expected_result
