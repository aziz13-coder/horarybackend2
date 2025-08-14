import datetime
import os
import sys

# Allow importing modules from the backend package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from horary_engine.engine import EnhancedTraditionalHoraryJudgmentEngine
from models import Planet


def test_will_he_marry_me_no_applying_aspect():
    engine = EnhancedTraditionalHoraryJudgmentEngine()

    # Chart data from Anthony Louis/Warnock "Will he marry me?" case
    dt_local = datetime.datetime(2004, 2, 3, 22, 0, 0)
    dt_utc = datetime.datetime(2004, 2, 4, 3, 0, 0)
    lat, lon = 38.9072, -77.0369

    chart = engine.calculator.calculate_chart(
        dt_local,
        dt_utc,
        "America/New_York",
        lat,
        lon,
        "Washington, DC, USA",
    )

    question_analysis = engine.question_analyzer.analyze_question("Will he marry me?")
    judgment = engine._apply_enhanced_judgment(chart, question_analysis)

    # Venus (L1) and Mars (L7) should not have an applying aspect
    assert engine._find_applying_aspect(chart, Planet.VENUS, Planet.MARS) is None
    assert judgment["result"] == "NO"
    reasoning_text = " ".join(judgment["reasoning"]).lower()
    assert "no perfection" in reasoning_text or "denial" in reasoning_text
