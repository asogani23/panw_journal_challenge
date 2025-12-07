# Aagam Sogani – PANW Intern Engineer Challenge (Option 1: AI-Powered Journaling)
# Wellbeing analyzer: maps free-form text to mood/energy/stress tags.

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

    def analyze(self, text: str) -> AnalysisResult:
        stripped = text.strip()
        if not stripped:
            return AnalysisResult(
                tags={
                    "mood": "neutral",
                    "energy": "low",
                    "stress": "unknown",
                },
                scores={
                    "note": "empty entry",
                },
            )

        sentiment_scores = self._sentiment.polarity_scores(stripped)
        mood = self._mood_from_sentiment(sentiment_scores["compound"])

        energy_index = self._energy_index(stripped)
        energy = self._bucket_energy(energy_index)

        stress = self._stress_level(mood, energy, stripped)

        mood, energy, stress = self._ambiguity_overrides(
            stripped, mood, energy, stress, sentiment_scores
        )

        return AnalysisResult(
            tags={
                "mood": mood,
                "energy": energy,
                "stress": stress,
            },
            scores={
                "sentiment": sentiment_scores,
                "energy_index": round(energy_index, 3),
            },
        )

    @staticmethod
    def _mood_from_sentiment(compound: float) -> str:
        if compound >= 0.4:
            return "positive"
        if compound <= -0.4:
            return "negative"
        return "neutral"

    @staticmethod
    def _energy_index(text: str) -> float:
        exclamations = text.count("!")
        words = [w for w in text.split() if any(c.isalpha() for c in w)]
        if not words:
            return 0.0

        caps_words = [
            w for w in words
            if len(w) > 2 and w.isupper()
        ]

        ex_factor = min(exclamations / 3.0, 1.0)
        caps_factor = min(len(caps_words) / len(words), 1.0)

        raw = ex_factor * 0.6 + caps_factor * 0.4
        return max(0.0, min(raw, 1.0))

    @staticmethod
    def _bucket_energy(score: float) -> str:
        if score < 0.3:
            return "low"
        if score < 0.7:
            return "medium"
        return "high"

    @staticmethod
    def _stress_level(mood: str, energy: str, text: str) -> str:
        lowered = text.lower()

        if any(w in lowered for w in ["overwhelmed", "stressed", "anxious", "panic", "burned out"]):
            return "high"

        if mood == "negative" and energy == "high":
            return "high"
        if mood == "negative" and energy == "low":
            return "drained"
        if mood == "positive" and energy == "high":
            return "engaged"

        return "moderate"

    @staticmethod
    def _ambiguity_overrides(
        text: str,
        mood: str,
        energy: str,
        stress: str,
        sentiment_scores: Dict[str, float],
    ):
        lowered = text.lower()

        if "crushing" in lowered:
            if "crushing it" in lowered or "crushing at" in lowered:
                mood = "positive"
                if energy == "low":
                    energy = "medium"
                stress = "engaged"
            elif "crushing me" in lowered or "crushing my" in lowered:
                mood = "negative"
                stress = "high"
                if sentiment_scores["compound"] > -0.4:
                    sentiment_scores["compound"] = -0.5

        return mood, energy, stress
