import os
import sys
import datetime as real_datetime

# Allow importing modules from the backend package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from question_analyzer import TraditionalHoraryQuestionAnalyzer


def test_specific_month_detection(monkeypatch):
    class FixedDateTime(real_datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2024, 6, 15)

    monkeypatch.setattr(real_datetime, "datetime", FixedDateTime)

    analyzer = TraditionalHoraryQuestionAnalyzer()
    result = analyzer.analyze_question("Will I get a job in September?")
    timeframe = result["timeframe_analysis"]

    assert timeframe["has_timeframe"] is True
    assert timeframe["type"] == "specific_month"
    assert timeframe["end_date"].year == 2024
    assert timeframe["end_date"].month == 9
    assert timeframe["end_date"].day == 30
