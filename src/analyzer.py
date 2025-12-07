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
class JournalAnalyzer:
    """
    Handles the NLP logic for the journaling app.
    """

    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_entry(self, text: str) -> Dict[str, Any]:
        """
        Analyzes the text for sentiment and generates contextual tags.
        
        We use VADER here because it is rule-based and specifically tuned 
        for social media data (emojis, capitalization), making it more 
        robust for journaling than a standard Naive Bayes classifier.
        """
        if not text or not text.strip():
            return {
                "sentiment": "Neutral",
                "score": 0.0,
                "tags": ["Empty"]
            }

        # VADER returns a compound score from -1 (Extremely Negative) 
        # to 1 (Extremely Positive).
        scores = self.analyzer.polarity_scores(text)
        compound = scores['compound']

        # Determine Primary Label
        # Thresholds based on standard VADER documentation (+/- 0.05 is neutral)
        label = "Neutral"
        if compound >= 0.05:
            label = "Positive"
        elif compound <= -0.05:
            label = "Negative"

        tags = [label]
        
        # CRITICAL LOGIC: Handling Ambiguity
        # We look for high-intensity scores to distinguish between
        # "crushing it" (High Positive) and "crushing me" (High Negative).
        # A threshold of 0.75 indicates strong emotional intensity.
        if compound >= 0.75:
            tags.append("High Energy")
        elif compound <= -0.75:
            tags.append("High Stress")

        return {
            "sentiment": label,
            "score": compound,
            "tags": tags
        }
       
