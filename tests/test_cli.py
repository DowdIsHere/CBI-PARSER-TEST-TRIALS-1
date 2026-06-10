"""CLI smoke tests: declaration, the pre-model refusal, and manual logging."""

import json

import pytest

from cbi_widget import cli


@pytest.fixture(autouse=True)
def isolated_data(tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "DATA", tmp_path)
    monkeypatch.setattr(cli, "STORE_PATH", tmp_path / "placements.json")
    monkeypatch.setattr(cli, "LAST_READ_PATH", tmp_path / "last_read.md")
    monkeypatch.setattr(cli, "TRACKER_PATH", tmp_path / "tracker.jsonl")
    return tmp_path


def test_declare_and_show(capsys):
    rc = cli.main([
        "declare", "--player", "Alice",
        "--spatial", "Abstract", "--temporal", "Future", "--reference", "Self",
        "--method", "independence", "--tier", "LOCKED",
        "--domains", "speech,tactical,habits", "--date", "2026-05-01",
        "--declared-by", "Robert",
    ])
    assert rc == 0
    rc = cli.main(["show"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Abstract" in out and "LOCKED" in out


def test_read_refuses_before_any_model_exists(capsys):
    # No placements declared, no API key, no SDK needed: the gate refuses first.
    rc = cli.main([
        "read", "--player-a", "Alice", "--player-b", "Bona",
        "--conditions", "indoor hard",
    ])
    assert rc == 2
    out = capsys.readouterr().out
    assert "no read is produced" in out


def test_log_requires_the_literal_it(tmp_path, capsys):
    cli.LAST_READ_PATH.write_text("# CBI Playbook Analysis: A vs. B\n")
    rc = cli.main(["log", "this", "--note", "x"])
    assert rc == 2
    rc = cli.main(["log", "it", "--note", "post-match"])
    assert rc == 0
    rows = [json.loads(l) for l in cli.TRACKER_PATH.read_text().splitlines()]
    assert rows[0]["note"] == "post-match"


def test_log_with_nothing_to_log(capsys):
    rc = cli.main(["log", "it"])
    assert rc == 2
    assert "Nothing to log" in capsys.readouterr().out
