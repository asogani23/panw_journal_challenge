from dataclasses import dataclass
from typing import Dict, Any
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

@dataclass
class AnalysisResult:
    tags: Dict[str, str]
    scores: Dict[str, Any]

class WellbeingAnalyzer:
    def __init__(self) -> None:
        self._sentiment = SentimentIntensityAnalyzer()

    # Stubbing the new method signature
    def analyze(self, text: str) -> AnalysisResult:
        return AnalysisResult(tags={}, scores={})
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
       
