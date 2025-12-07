# Aagam Sogani – PANW Intern Engineer Challenge
# CLI entry point: wires analyzer and storage into a simple journaling tool.

import argparse
from pathlib import Path

def main() -> None:
    pass

if __name__ == "__main__":
    main()
# ... imports ...

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="AI powered journaling CLI that tags mental well being from free form text."
    )

    parser.add_argument(
        "--file",
        type=str,
        help="Optional path to JSON storage (default: data/journal_entries.json).",
    )
    # ... inside build_parser ...
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new journal entry.")
    add_parser.add_argument(
        "text",
        type=str,
        help="Journal text (wrap in quotes).",
    )

    summary_parser = subparsers.add_parser(
        "summary", help="Show a summary of recent entries."
    )
    summary_parser.add_argument(
        "--last",
        type=int,
        default=3,
        help="Number of entries to show (default: 3).",
    )

    return parser
    
    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

# ... imports ...

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="AI powered journaling CLI that tags mental well being from free form text."
    )

    parser.add_argument(
        "--file",
        type=str,
        help="Optional path to JSON storage (default: data/journal_entries.json).",
    )
    
    return parser


# ... inside show_summary(args) ...
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
        # Scores printing coming in next commit for cleaner diff

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
