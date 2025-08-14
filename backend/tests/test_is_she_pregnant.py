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


def test_pregnancy_house_derivation():
    analyzer = TraditionalHoraryQuestionAnalyzer()
    result = analyzer.analyze_question("Is she pregnant?")
    assert result["relevant_houses"] == [1, 7, 11]
    assert result["significators"]["quesited_house"] == 11
