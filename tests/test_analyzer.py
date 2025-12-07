# Aagam Sogani - PANW Intern Engineer Challenge
# Tests for the WellbeingAnalyzer (ambiguity, empty text, stress words).

import pytest

from src.analyzer import WellbeingAnalyzer


@pytest.fixture
def analyzer():
    return WellbeingAnalyzer()

