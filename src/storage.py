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
