from dataclasses import dataclass
from typing import Dict, Any
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

@dataclass
class AnalysisResult:
    tags: Dict[str, str]
    scores: Dict[str, Any]

# ... imports and dataclass ...

class WellbeingAnalyzer:
    # ... __init__ ...

    # ... analyze method ...

    @staticmethod
    def _mood_from_sentiment(compound: float) -> str:
        if compound >= 0.4:
            return "positive"
        if compound <= -0.4:
            return "negative"
        return "neutral"

    @staticmethod
    def _energy_index(text: str) -> float:
        """Calculates energy based on exclamation marks and capitalization intensity."""
        exclamations = text.count("!")
        words = [w for w in text.split() if any(c.isalpha() for c in w)]
        if not words:
            return 0.0

        caps_words = [w for w in words if len(w) > 2 and w.isupper()]
        
        ex_factor = min(exclamations / 3.0, 1.0)
        caps_factor = min(len(caps_words) / len(words), 1.0)
        
        # Weighted average: 60% punctuation, 40% capitalization
        raw = ex_factor * 0.6 + caps_factor * 0.4
        return max(0.0, min(raw, 1.0))

    @staticmethod
    def _bucket_energy(score: float) -> str:
        if score < 0.3: return "low"
        if score < 0.7: return "medium"
        return "high"

