# Aagam Sogani – PANW Intern Engineer Challenge
# Journal storage: JSON-based persistence for entries.

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any


@dataclass
class Entry:
    id: int
    created_at: str
    text: str
    tags: Dict[str, str]
    scores: Dict[str, Any]


class JournalStorage:
    def __init__(self, path: Path) -> None:
        self.path = path

    def _ensure_file(self) -> None:
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text("[]", encoding="utf-8")

    def load_entries(self) -> List[Entry]:
        self._ensure_file()
        raw = self.path.read_text(encoding="utf-8").strip()
        if not raw:
            return []

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return []

        entries: List[Entry] = []
        for item in data:
            entries.append(
                Entry(
                    id=item.get("id", 0),
                    created_at=item.get("created_at", ""),
                    text=item.get("text", ""),
                    tags=item.get("tags", {}),
                    scores=item.get("scores", {}),
                )
            )
        return entries

    def save_entries(self, entries: List[Entry]) -> None:
        serializable = [asdict(e) for e in entries]
        self.path.write_text(json.dumps(serializable, indent=2), encoding="utf-8")

    def next_id(self, entries: List[Entry]) -> int:
        if not entries:
            return 1
        return max(e.id for e in entries) + 1

    @staticmethod
    def now_utc_iso() -> str:
        return datetime.now(timezone.utc).isoformat()
