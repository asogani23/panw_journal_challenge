# Aagam Sogani - PANW Intern Engineer Challenge
# Tests for the WellbeingAnalyzer (ambiguity, empty text, stress words).

import pytest

from src.analyzer import WellbeingAnalyzer


@pytest.fixture
def analyzer():
    return WellbeingAnalyzer()


def test_crushing_it_is_positive_and_engaged(analyzer):
    text = "I am absolutely CRUSHING IT at work today! 🔥"
    result = analyzer.analyze(text)
    assert result.tags["mood"] == "positive"
    assert result.tags["stress"] == "engaged"
    assert result.tags["energy"] in ("medium", "high")

def test_crushing_me_is_negative_and_high_stress(analyzer):
    text = "The workload is crushing me and I am so stressed out..."
    result = analyzer.analyze(text)
    assert result.tags["mood"] == "negative"
    assert result.tags["stress"] == "high"
