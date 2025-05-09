import sys

import pytest

from services import parse_args


def test_parse_args_valid(monkeypatch):
    test_args = ["script_name.py", "file1.csv", "file2.csv", "--report", "payout"]
    monkeypatch.setattr(sys, "argv", test_args)
    result = parse_args()
    assert result == {
        "files": ["file1.csv", "file2.csv"],
        "report": "payout",
    }


def test_parse_args_missing_report(monkeypatch):
    test_args = ["script_name.py", "file1.csv"]
    monkeypatch.setattr(sys, "argv", test_args)
    with pytest.raises(SystemExit):
        parse_args()
