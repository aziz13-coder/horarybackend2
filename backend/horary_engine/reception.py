"""Reception calculations for the horary engine."""

from typing import Dict, List, Tuple, Any

from models import Planet, Sign, HoraryChart


class TraditionalReceptionCalculator:
    """Centralized reception calculator - single source of truth for all reception logic"""

    def __init__(self) -> None:
        # Traditional exaltations
        self.exaltations = {
            Planet.SUN: Sign.ARIES,
            Planet.MOON: Sign.TAURUS,
            Planet.MERCURY: Sign.VIRGO,
            Planet.VENUS: Sign.PISCES,
            Planet.MARS: Sign.CAPRICORN,
            Planet.JUPITER: Sign.CANCER,
            Planet.SATURN: Sign.LIBRA,
        }

        # Traditional triplicity rulers (day/night)
        self.triplicity_rulers = {
            # Fire signs (Aries, Leo, Sagittarius)
            Sign.ARIES: {"day": Planet.SUN, "night": Planet.JUPITER},
            Sign.LEO: {"day": Planet.SUN, "night": Planet.JUPITER},
            Sign.SAGITTARIUS: {"day": Planet.SUN, "night": Planet.JUPITER},

            # Earth signs (Taurus, Virgo, Capricorn)
            Sign.TAURUS: {"day": Planet.VENUS, "night": Planet.MOON},
            Sign.VIRGO: {"day": Planet.VENUS, "night": Planet.MOON},
            Sign.CAPRICORN: {"day": Planet.VENUS, "night": Planet.MOON},

            # Air signs (Gemini, Libra, Aquarius)
            Sign.GEMINI: {"day": Planet.SATURN, "night": Planet.MERCURY},
            Sign.LIBRA: {"day": Planet.SATURN, "night": Planet.MERCURY},
            Sign.AQUARIUS: {"day": Planet.SATURN, "night": Planet.MERCURY},

            # Water signs (Cancer, Scorpio, Pisces)
            Sign.CANCER: {"day": Planet.MARS, "night": Planet.VENUS},
            Sign.SCORPIO: {"day": Planet.MARS, "night": Planet.VENUS},
            Sign.PISCES: {"day": Planet.MARS, "night": Planet.VENUS},
        }

    def calculate_comprehensive_reception(
        self, chart: HoraryChart, planet1: Planet, planet2: Planet
    ) -> Dict[str, Any]:
        """SINGLE SOURCE OF TRUTH for all reception calculations
        Returns comprehensive reception data used by both reasoning and structured output."""

        # Get planet positions
        pos1 = chart.planets[planet1]
        pos2 = chart.planets[planet2]

        # Determine day/night for triplicity calculations
        sun_pos = chart.planets[Planet.SUN]
        sun_house = self._calculate_house_position(sun_pos.longitude, chart.houses)
        is_day = sun_house in [7, 8, 9, 10, 11, 12]  # Sun below horizon = day chart

        # Check all dignity types for both directions
        reception_1_to_2 = self._check_all_dignities(planet1, pos2, is_day)
        reception_2_to_1 = self._check_all_dignities(planet2, pos1, is_day)

        # Determine overall reception type
        reception_type, reception_details = self._classify_reception(
            planet1, planet2, reception_1_to_2, reception_2_to_1
        )

        return {
            "type": reception_type,  # none, mutual_rulership, mutual_exaltation, mixed_reception, unilateral
            "details": reception_details,
            "planet1_receives_planet2": reception_1_to_2,
            "planet2_receives_planet1": reception_2_to_1,
            "day_chart": is_day,
            "display_text": self._format_reception_display(
                reception_type, planet1, planet2, reception_details
            ),
            "traditional_strength": self._calculate_reception_strength(
                reception_type, reception_details
            ),
        }

    def _check_all_dignities(
        self, receiving_planet: Planet, received_position, is_day: bool
    ) -> List[str]:
        """Check all traditional dignity types for reception"""
        dignities: List[str] = []

        # 1. Domicile/Rulership (strongest)
        if received_position.sign.ruler == receiving_planet:
            dignities.append("domicile")

        # 2. Exaltation (second strongest)
        if (
            receiving_planet in self.exaltations
            and self.exaltations[receiving_planet] == received_position.sign
        ):
            dignities.append("exaltation")

        # 3. Triplicity (third strongest)
        if self._has_triplicity_dignity(receiving_planet, received_position.sign, is_day):
            dignities.append("triplicity")

        # TODO: Could add terms and faces for complete traditional reception
        # 4. Terms (Egyptian terms)
        # 5. Faces/Decans

        return dignities

    def _has_triplicity_dignity(self, planet: Planet, sign: Sign, is_day: bool) -> bool:
        """Check if planet has triplicity dignity in sign"""
        if sign not in self.triplicity_rulers:
            return False

        sect = "day" if is_day else "night"
        return self.triplicity_rulers[sign][sect] == planet

    def _classify_reception(
        self,
        planet1: Planet,
        planet2: Planet,
        reception_1_to_2: List[str],
        reception_2_to_1: List[str],
    ) -> Tuple[str, Dict]:
        """Classify the overall reception type"""

        # No reception
        if not reception_1_to_2 and not reception_2_to_1:
            return "none", {}

        # Mutual reception - same dignity type both ways
        if "domicile" in reception_1_to_2 and "domicile" in reception_2_to_1:
            return "mutual_rulership", {
                "planet1_dignities": reception_1_to_2,
                "planet2_dignities": reception_2_to_1,
            }

        if "exaltation" in reception_1_to_2 and "exaltation" in reception_2_to_1:
            return "mutual_exaltation", {
                "planet1_dignities": reception_1_to_2,
                "planet2_dignities": reception_2_to_1,
            }

        # Mixed mutual reception - different dignity types
        if reception_1_to_2 and reception_2_to_1:
            return "mixed_reception", {
                "planet1_dignities": reception_1_to_2,
                "planet2_dignities": reception_2_to_1,
            }

        # Unilateral reception - one way only
        if reception_1_to_2:
            return "unilateral", {
                "receiving_planet": planet1,
                "received_planet": planet2,
                "dignities": reception_1_to_2,
            }
        else:
            return "unilateral", {
                "receiving_planet": planet2,
                "received_planet": planet1,
                "dignities": reception_2_to_1,
            }

    def _format_reception_display(
        self, reception_type: str, planet1: Planet, planet2: Planet, details: Dict
    ) -> str:
        """Format reception for display in reasoning"""
        if reception_type == "none":
            return "no reception"
        if reception_type == "mutual_rulership":
            return f"{planet1.value}↔{planet2.value} mutual domicile reception"
        if reception_type == "mutual_exaltation":
            return f"{planet1.value}↔{planet2.value} mutual exaltation reception"
        if reception_type == "mixed_reception":
            p1_dignities = ", ".join(details.get("planet1_dignities", []))
            p2_dignities = ", ".join(details.get("planet2_dignities", []))
            return (
                f"{planet1.value}↔{planet2.value} mixed reception ({p1_dignities} / {p2_dignities})"
            )
        if reception_type == "unilateral":
            receiving = details.get("receiving_planet")
            received = details.get("received_planet")
            dignities = ", ".join(details.get("dignities", []))
            return f"{receiving.value} receives {received.value} by {dignities}"
        return f"{reception_type} reception"

    def _calculate_reception_strength(self, reception_type: str, details: Dict) -> int:
        """Calculate numerical strength of reception for confidence calculations"""
        if reception_type == "none":
            return 0
        if reception_type == "mutual_rulership":
            return 10  # Strongest
        if reception_type == "mutual_exaltation":
            return 8
        if reception_type == "mixed_reception":
            return 6
        if reception_type == "unilateral":
            dignities = details.get("dignities", [])
            if "domicile" in dignities:
                return 5
            if "exaltation" in dignities:
                return 4
            if "triplicity" in dignities:
                return 3
            return 2
        return 1

    def _calculate_house_position(self, longitude: float, houses: List[float]) -> int:
        """Helper method for house calculation"""
        longitude = longitude % 360

        for i in range(12):
            current_cusp = houses[i] % 360
            next_cusp = houses[(i + 1) % 12] % 360

            if current_cusp > next_cusp:  # Crosses 0°
                if longitude >= current_cusp or longitude < next_cusp:
                    return i + 1
            else:
                if current_cusp <= longitude < next_cusp:
                    return i + 1

        return 1
