import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

# ... imports ...

@dataclass
class Entry:
    id: int
    created_at: str
    text: str
    tags: Dict[str, str]
    scores: Dict[str, Any]
# ... Entry class ...

class JournalStorage:
    def __init__(self, path: Path) -> None:
        self.path = path
        
    # ... inside JournalStorage ...
    def _ensure_file(self) -> None:
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text("[]", encoding="utf-8")
    # ... inside JournalStorage ...
    def _ensure_file(self) -> None:
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text("[]", encoding="utf-8")
    

    def save_entries(self, entries: List[Entry]) -> None:
        serializable = [asdict(e) for e in entries]
        self.path.write_text(json.dumps(serializable, indent=2), encoding="utf-8")
