from expense_tracker.cli import main


def test_add_then_summary(tmp_path, capsys):
    f = str(tmp_path / "e.json")
    assert main(["--file", f, "add", "250", "travel", "--note", "bus pass"]) == 0
    assert main(["--file", f, "add", "80", "food"]) == 0
    capsys.readouterr()

    assert main(["--file", f, "summary"]) == 0
    out = capsys.readouterr().out
    assert "travel" in out
    assert "330.00" in out


def test_invalid_amount_returns_error(tmp_path, capsys):
    f = str(tmp_path / "e.json")
    assert main(["--file", f, "add", "-1", "food"]) == 1
    assert "error" in capsys.readouterr().err
