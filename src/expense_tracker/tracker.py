import json
from datetime import date
from pathlib import Path


class ExpenseError(ValueError):
    """Raised when an expense entry is not valid."""


def make_expense(amount, category, note="", on=None):
    """Build one expense record as a dict."""
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        raise ExpenseError("amount must be a number")
    if amount <= 0:
        raise ExpenseError("amount must be greater than zero")

    category = str(category).strip().lower()
    if not category:
        raise ExpenseError("category cannot be empty")

    return {
        "amount": round(amount, 2),
        "category": category,
        "note": note.strip(),
        "date": (on or date.today()).isoformat(),
    }


def total(expenses):
    return round(sum(e["amount"] for e in expenses), 2)


def total_by_category(expenses):
    result = {}
    for e in expenses:
        result[e["category"]] = round(result.get(e["category"], 0) + e["amount"], 2)
    return result


def load(path):
    path = Path(path)
    if not path.exists():
        return []
    with path.open() as f:
        return json.load(f)


def save(path, expenses):
    with Path(path).open("w") as f:
        json.dump(expenses, f, indent=2)
