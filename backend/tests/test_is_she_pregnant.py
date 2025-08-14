import os
import sys

# Allow importing modules from the backend package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from question_analyzer import TraditionalHoraryQuestionAnalyzer
import pytest


@pytest.mark.parametrize(
    "question",
    [
        "Is she pregnant?",
        "Is he lying?",
        "Is they happy?",
    ],
)
def test_direct_pronoun_detection(question):
    analyzer = TraditionalHoraryQuestionAnalyzer()
    result = analyzer.analyze_question(question)
    assert result["third_person_analysis"]["is_third_person"] is True
