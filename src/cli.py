# Aagam Sogani – PANW Intern Engineer Challenge
# CLI entry point: wires analyzer and storage into a simple journaling tool.

import argparse
from pathlib import Path

from .analyzer import WellbeingAnalyzer
from .storage import JournalStorage, Entry


DEFAULT_DATA_PATH = Path("data") / "journal_entries.json"


def add_entry(args) -> None:
    storage_path = Path(args.file) if args.file else DEFAULT_DATA_PATH
    storage = JournalStorage(storage_path)
    analyzer = WellbeingAnalyzer()

    entries = storage.load_entries()
    new_id = storage.next_id(entries)

    analysis = analyzer.analyze(args.text)
    entry = Entry(
        id=new_id,
        created_at=JournalStorage.now_utc_iso(),
        text=args.text,
        tags=analysis.tags,
        scores=analysis.scores,
    )

    entries.append(entry)
    storage.save_entries(entries)

    print(f"Saved entry #{entry.id} to {storage_path}")
    print("Tags:")
    for k, v in analysis.tags.items():
        print(f"  - {k}: {v}")
    print("Scores:")
    for k, v in analysis.scores.items():
        print(f"  - {k}: {v}")


def show_summary(args) -> None:
    storage_path = Path(args.file) if args.file else DEFAULT_DATA_PATH
    storage = JournalStorage(storage_path)
    entries = storage.load_entries()

    if not entries:
        print(f"No entries found in {storage_path}. Try adding one with 'add'.")
        return

    n = args.last
    to_show = entries[-n:]

    print(f"Last {len(to_show)} entries from {storage_path}:")
    for entry in to_show:
        print("=" * 40)
        print(f"#{entry.id} @ {entry.created_at}")
        print(entry.text)
        print("Tags:")
        for k, v in entry.tags.items():
            print(f"  - {k}: {v}")

        energy_index = entry.scores.get("energy_index")
        sentiment = entry.scores.get("sentiment")

        print("Scores:")
        if energy_index is not None:
            print(f"  - energy_index: {energy_index}")
        if sentiment:
            print(
                "  - sentiment "
                f"(compound={sentiment.get('compound')}, "
                f"pos={sentiment.get('pos')}, "
                f"neu={sentiment.get('neu')}, "
                f"neg={sentiment.get('neg')})"
            )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="AI powered journaling CLI that tags mental well being from free form text."
    )

    parser.add_argument(
        "--file",
        type=str,
        help="Optional path to JSON storage (default: data/journal_entries.json).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new journal entry.")
    add_parser.add_argument(
        "text",
        type=str,
        help="Journal text (wrap in quotes).",
    )
    add_parser.set_defaults(func=add_entry)

    summary_parser = subparsers.add_parser(
        "summary", help="Show a summary of recent entries."
    )
    summary_parser.add_argument(
        "--last",
        type=int,
        default=3,
        help="Number of entries to show (default: 3).",
    )
    summary_parser.set_defaults(func=show_summary)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
