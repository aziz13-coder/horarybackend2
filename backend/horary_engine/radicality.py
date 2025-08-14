"""Radicality checks for horary charts."""

from typing import Any, Dict

from horary_config import cfg
from models import HoraryChart, Planet, Sign


def check_enhanced_radicality(chart: HoraryChart, ignore_saturn_7th: bool = False) -> Dict[str, Any]:
    """Enhanced radicality checks with configuration"""

    config = cfg()
    asc_degree = chart.ascendant % 30

    # Too early
    if asc_degree < config.radicality.asc_too_early:
        return {
            "valid": False,
            "reason": f"Ascendant too early at {asc_degree:.1f}° - question premature or not mature",
        }

    # Too late
    if asc_degree > config.radicality.asc_too_late:
        return {
            "valid": False,
            "reason": f"Ascendant too late at {asc_degree:.1f}° - question too late or already decided",
        }

    # Saturn in 7th house (configurable)
    if config.radicality.saturn_7th_enabled and not ignore_saturn_7th:
        saturn_pos = chart.planets[Planet.SATURN]
        if saturn_pos.house == 7:
            return {
                "valid": False,
                "reason": "Saturn in 7th house - astrologer may err in judgment (Bonatti)",
            }

    # Via Combusta (configurable)
    if config.radicality.via_combusta_enabled:
        moon_pos = chart.planets[Planet.MOON]
        moon_degree_in_sign = moon_pos.longitude % 30

        via_combusta = config.radicality.via_combusta

        if (
            (moon_pos.sign == Sign.LIBRA and moon_degree_in_sign > via_combusta.libra_start)
            or (
                moon_pos.sign == Sign.SCORPIO
                and moon_degree_in_sign <= via_combusta.scorpio_end
            )
        ):
            return {
                "valid": False,
                "reason": (
                    f"Moon in Via Combusta ({moon_pos.sign.sign_name} {moon_degree_in_sign:.1f}°) - "
                    "volatile or corrupted matter"
                ),
            }

    return {
        "valid": True,
        "reason": f"Chart is radical - Ascendant at {asc_degree:.1f}°",
    }
