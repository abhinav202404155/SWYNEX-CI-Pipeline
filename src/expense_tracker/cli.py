import argparse
import sys

from . import tracker

DEFAULT_FILE = "expenses.json"


def build_parser():
    parser = argparse.ArgumentParser(prog="expense-tracker")
    parser.add_argument("--file", default=DEFAULT_FILE, help="json file used for storage")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="add an expense")
    add.add_argument("amount")
    add.add_argument("category")
    add.add_argument("--note", default="")

    sub.add_parser("summary", help="show totals per category")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    expenses = tracker.load(args.file)

    if args.command == "add":
        try:
            expenses.append(tracker.make_expense(args.amount, args.category, args.note))
        except tracker.ExpenseError as err:
            print(f"error: {err}", file=sys.stderr)
            return 1
        tracker.save(args.file, expenses)
        print("saved")
        return 0

    for category, amount in sorted(tracker.total_by_category(expenses).items()):
        print(f"{category:<15}{amount:>10.2f}")
    print(f"{'total':<15}{tracker.total(expenses):>10.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
