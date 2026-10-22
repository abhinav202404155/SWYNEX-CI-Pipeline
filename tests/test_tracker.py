from datetime import date

import pytest

from expense_tracker import tracker


def test_make_expense_normalises_fields():
    e = tracker.make_expense("120.456", "  Food ", " lunch ", on=date(2026, 10, 1))
    assert e == {"amount": 120.46, "category": "food", "note": "lunch", "date": "2026-10-01"}


@pytest.mark.parametrize("bad", [0, -5, "abc", None])
def test_bad_amount_rejected(bad):
    with pytest.raises(tracker.ExpenseError):
        tracker.make_expense(bad, "food")


def test_empty_category_rejected():
    with pytest.raises(tracker.ExpenseError):
        tracker.make_expense(10, "   ")


def test_totals():
    items = [
        tracker.make_expense(100, "food"),
        tracker.make_expense(50.5, "food"),
        tracker.make_expense(200, "travel"),
    ]
    assert tracker.total(items) == 350.5
    assert tracker.total_by_category(items) == {"food": 150.5, "travel": 200}


def test_save_and_load_roundtrip(tmp_path):
    f = tmp_path / "data.json"
    items = [tracker.make_expense(10, "misc")]
    tracker.save(f, items)
    assert tracker.load(f) == items


def test_load_missing_file_gives_empty_list(tmp_path):
    assert tracker.load(tmp_path / "nope.json") == []
