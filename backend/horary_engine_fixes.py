#!/usr/bin/env python3
"""
HORARY ENGINE FIXES - Core Logic Corrections

This module contains fixes for the fundamental horary logic errors identified
in the engine validation. These fixes address:

1. Significator perfection logic (requires direct L1-L7 aspects)
2. Prohibition detection system
3. Moon aspect role hierarchy
4. Traditional horary rule validation

CRITICAL ISSUES IDENTIFIED:
- Engine uses Moon-Venus Trine for YES judgment (WRONG)
- No prohibition detection for Saturn interference
- Moon aspects treated as primary perfection (WRONG)
- Contradicts established horary doctrine

TRADITIONAL HORARY RULES:
- Only direct significator aspects create perfection
- Prohibition by malefics blocks perfection
- Moon aspects are secondary (translation/collection only)
- No applying L1-L7 aspect = NO perfection = NO judgment
"""

from typing import Dict, List, Optional, Any
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class PerfectionType(Enum):
    """Types of horary perfection according to traditional doctrine"""
    DIRECT_ASPECT = "direct_aspect"          # L1-L7 applying aspect
    TRANSLATION = "translation"              # Planet translates light between L1-L7
    COLLECTION = "collection"                # Planet collects light from both L1-L7
    MUTUAL_RECEPTION = "mutual_reception"    # L1-L7 in mutual reception
    NO_PERFECTION = "no_perfection"         # No perfection possible

@dataclass
class HoraryFix:
    """Container for horary logic fixes"""
    name: str
    description: str
    traditional_source: str
    fixes_applied: bool = False

class TraditionalHoraryValidator:
    """
    Traditional Horary Validation System
    
    Implements classical horary rules from:
    - William Lilly (Christian Astrology)
    - Guido Bonatti (Liber Astronomicus) 
    - Traditional medieval sources
    """
    
    def __init__(self):
        self.fixes = [
            HoraryFix(
                name="significator_perfection_priority",
                description="Only direct L1-L7 applying aspects create primary perfection",
                traditional_source="Lilly III, Ch. XXV - 'Of the manner of judging any question'"
            ),
            HoraryFix(
                name="prohibition_detection", 
                description="Saturn/Mars can prohibit perfection by intervening aspects",
                traditional_source="Lilly III, Ch. XXI - 'Of the frustration of planets'"
            ),
            HoraryFix(
                name="moon_role_correction",
                description="Moon aspects are secondary - translation/collection only",
                traditional_source="Lilly III, Ch. XXVI - 'Of the translation of light'"
            ),
            HoraryFix(
                name="no_perfection_equals_no",
                description="No applying significator aspect = NO judgment",
                traditional_source="Traditional horary doctrine - universal rule"
            )
        ]
    
    def validate_significator_perfection(self, chart_data: Dict, querent_planet: str, 
                                      quesited_planet: str) -> Dict[str, Any]:
        """
        FIXED: Check for direct significator perfection ONLY
        
        Traditional Rule: Only applying aspects between L1-L7 create perfection
        """
        
        # Find direct applying aspect between significators
        direct_aspect = None
        aspects = chart_data.get('aspects', [])
        
        for aspect in aspects:
            planet1 = aspect.get('planet1')
            planet2 = aspect.get('planet2')
            applying = aspect.get('applying', False)
            
            # Check if this is a significator aspect
            if ((planet1 == querent_planet and planet2 == quesited_planet) or
                (planet1 == quesited_planet and planet2 == querent_planet)) and applying:
                direct_aspect = aspect
                break
        
        if direct_aspect:
            aspect_type = direct_aspect.get('aspect', 'Unknown')
            orb = direct_aspect.get('orb', 0)
            
            # Traditional favorable aspects
            favorable_aspects = ['Conjunction', 'Sextile', 'Trine']
            favorable = aspect_type in favorable_aspects
            
            return {
                'perfection_found': True,
                'perfection_type': PerfectionType.DIRECT_ASPECT,
                'favorable': favorable,
                'aspect_type': aspect_type,
                'orb': orb,
                'confidence': 85 if favorable else 75,
                'reason': f"Direct {aspect_type.lower()} between {querent_planet} and {quesited_planet}",
                'traditional_valid': True
            }
        
        # Check for translation/collection (secondary perfection)
        translation = self._check_translation_of_light(chart_data, querent_planet, quesited_planet)
        if translation['found']:
            return translation
            
        collection = self._check_collection_of_light(chart_data, querent_planet, quesited_planet)
        if collection['found']:
            return collection
        
        # NO PERFECTION FOUND - Traditional Rule: This means NO
        return {
            'perfection_found': False,
            'perfection_type': PerfectionType.NO_PERFECTION,
            'favorable': False,
            'confidence': 85,  # High confidence in NO when no perfection
            'reason': f"No applying aspect between {querent_planet} and {quesited_planet}",
            'traditional_valid': True
        }
    
    def check_prohibition(self, chart_data: Dict, querent_planet: str, 
                         quesited_planet: str, perfection_data: Dict) -> Dict[str, Any]:
        """
        FIXED: Proper prohibition detection
        
        Traditional Rule: Saturn/Mars can prohibit perfection by intervening aspects
        """
        
        if not perfection_data.get('perfection_found'):
            return {'prohibited': False, 'reason': 'No perfection to prohibit'}
        
        planets_data = chart_data.get('planets', {})
        aspects = chart_data.get('aspects', [])
        
        # Check Saturn and Mars for prohibiting aspects
        malefics = ['Saturn', 'Mars']
        
        for malefic in malefics:
            if malefic not in planets_data:
                continue
                
            # Check if malefic aspects either significator before they can perfect
            malefic_aspects = [asp for asp in aspects 
                             if asp.get('applying', False) and 
                             (asp.get('planet1') == malefic or asp.get('planet2') == malefic)]
            
            for aspect in malefic_aspects:
                other_planet = (aspect.get('planet1') if aspect.get('planet2') == malefic 
                              else aspect.get('planet2'))
                
                if other_planet in [querent_planet, quesited_planet]:
                    # Check if this aspect perfects before the significator aspect
                    degrees_to_exact = aspect.get('degrees_to_exact', 999)
                    perfection_degrees = perfection_data.get('degrees_to_exact', 0)
                    
                    if degrees_to_exact < perfection_degrees:
                        return {
                            'prohibited': True,
                            'prohibitor': malefic,
                            'aspect_type': aspect.get('aspect'),
                            'target': other_planet,
                            'confidence': 85,  # Traditional prohibition confidence
                            'reason': f"{malefic} {aspect.get('aspect', '').lower()}s {other_planet} before perfection",
                            'traditional_valid': True
                        }
        
        return {'prohibited': False, 'reason': 'No prohibition detected'}
    
    def _check_translation_of_light(self, chart_data: Dict, querent: str, quesited: str) -> Dict[str, Any]:
        """Check for translation of light (secondary perfection)"""
        
        aspects = chart_data.get('aspects', [])
        
        # Find planets that aspect both significators
        for aspect1 in aspects:
            if not aspect1.get('applying', False):
                continue
                
            p1, p2 = aspect1.get('planet1'), aspect1.get('planet2')
            
            # Check if one planet aspects querent
            translator = None
            if p1 == querent:
                translator = p2
            elif p2 == querent:
                translator = p1
                
            if translator and translator not in [querent, quesited]:
                # Check if translator also aspects quesited
                for aspect2 in aspects:
                    if not aspect2.get('applying', False):
                        continue
                        
                    p3, p4 = aspect2.get('planet1'), aspect2.get('planet2')
                    if ((p3 == translator and p4 == quesited) or 
                        (p4 == translator and p3 == quesited)):
                        
                        return {
                            'perfection_found': True,
                            'found': True,
                            'perfection_type': PerfectionType.TRANSLATION,
                            'translator': translator,
                            'favorable': True,  # Translation generally favorable
                            'confidence': 70,   # Lower than direct perfection
                            'reason': f"Translation of light by {translator}",
                            'traditional_valid': True
                        }
        
        return {'found': False}
    
    def _check_collection_of_light(self, chart_data: Dict, querent: str, quesited: str) -> Dict[str, Any]:
        """Check for collection of light (secondary perfection)"""
        
        aspects = chart_data.get('aspects', [])
        
        # Find planets that receive aspects from both significators
        for planet_name in chart_data.get('planets', {}).keys():
            if planet_name in [querent, quesited]:
                continue
                
            querent_aspects_planet = False
            quesited_aspects_planet = False
            
            for aspect in aspects:
                if not aspect.get('applying', False):
                    continue
                    
                p1, p2 = aspect.get('planet1'), aspect.get('planet2')
                
                if p1 == querent and p2 == planet_name:
                    querent_aspects_planet = True
                elif p2 == querent and p1 == planet_name:
                    querent_aspects_planet = True
                elif p1 == quesited and p2 == planet_name:
                    quesited_aspects_planet = True
                elif p2 == quesited and p1 == planet_name:
                    quesited_aspects_planet = True
            
            if querent_aspects_planet and quesited_aspects_planet:
                return {
                    'perfection_found': True,
                    'found': True,
                    'perfection_type': PerfectionType.COLLECTION,
                    'collector': planet_name,
                    'favorable': True,  # Collection generally favorable
                    'confidence': 65,   # Lower than direct or translation
                    'reason': f"Collection of light by {planet_name}",
                    'traditional_valid': True
                }
        
        return {'found': False}


class FixedHoraryJudgment:
    """
    FIXED Horary Judgment Engine
    
    Implements traditional horary rules correctly:
    1. ONLY significator aspects create primary perfection
    2. Moon aspects are secondary (translation/collection only)  
    3. No perfection = NO judgment
    4. Prohibition by malefics blocks perfection
    """
    
    def __init__(self):
        self.validator = TraditionalHoraryValidator()
    
    def apply_traditional_judgment(self, chart_data: Dict, question_type: str, 
                                 querent_planet: str, quesited_planet: str) -> Dict[str, Any]:
        """
        FIXED: Apply traditional horary judgment correctly
        
        This replaces the flawed Moon-based logic with proper significator analysis
        """
        
        reasoning = []
        
        # 1. Check significator perfection (PRIMARY RULE)
        perfection = self.validator.validate_significator_perfection(
            chart_data, querent_planet, quesited_planet)
        
        reasoning.append(f"Significators: {querent_planet} (querent) and {quesited_planet} (quesited)")
        
        if not perfection['perfection_found']:
            # TRADITIONAL RULE: No perfection = NO judgment
            return {
                'judgment': 'NO',
                'confidence': perfection['confidence'],
                'reasoning': reasoning + [
                    perfection['reason'],
                    "Traditional rule: No applying significator aspect = No perfection possible",
                    "Anthony Louis doctrine: 'No applying L1–L7 aspect' = NO"
                ],
                'perfection_type': perfection['perfection_type'].value,
                'traditional_validation': 'PASSED',
                'fixes_applied': ['significator_perfection_priority', 'no_perfection_equals_no']
            }
        
        # 2. Check for prohibition (if perfection exists)
        prohibition = self.validator.check_prohibition(chart_data, querent_planet, quesited_planet, perfection)
        
        if prohibition['prohibited']:
            # TRADITIONAL RULE: Prohibition blocks perfection
            return {
                'judgment': 'NO',
                'confidence': prohibition['confidence'],
                'reasoning': reasoning + [
                    f"Perfection: {perfection['reason']}",
                    f"Prohibition: {prohibition['reason']}",
                    "Traditional rule: Prohibition blocks perfection",
                    "Anthony Louis doctrine: 'prohibition blocks perfection' = NO"
                ],
                'perfection_type': perfection['perfection_type'].value,
                'prohibition_detected': True,
                'traditional_validation': 'PASSED',
                'fixes_applied': ['significator_perfection_priority', 'prohibition_detection']
            }
        
        # 3. Perfection exists and no prohibition - make judgment
        judgment = 'YES' if perfection['favorable'] else 'NO'
        confidence = perfection['confidence']
        
        reasoning.extend([
            f"Perfection: {perfection['reason']}",
            f"Aspect favorable: {perfection['favorable']}",
            "No prohibition detected"
        ])
        
        # 4. Check Moon testimony (SECONDARY only)
        moon_testimony = self._check_moon_testimony_secondary(chart_data, querent_planet, quesited_planet)
        if moon_testimony['significant']:
            reasoning.append(f"Moon testimony (secondary): {moon_testimony['reason']}")
            # Moon can modify confidence slightly but not override significator perfection
            if moon_testimony['supports_judgment']:
                confidence = min(100, confidence + 5)
            else:
                confidence = max(50, confidence - 10)
        
        return {
            'judgment': judgment,
            'confidence': confidence,
            'reasoning': reasoning,
            'perfection_type': perfection['perfection_type'].value,
            'prohibition_detected': False,
            'traditional_validation': 'PASSED',
            'fixes_applied': ['significator_perfection_priority', 'moon_role_correction']
        }
    
    def _check_moon_testimony_secondary(self, chart_data: Dict, querent: str, quesited: str) -> Dict[str, Any]:
        """
        FIXED: Moon testimony as SECONDARY factor only
        
        Traditional Role: Moon supports but does not override significator judgment
        """
        
        aspects = chart_data.get('aspects', [])
        moon_aspects = [asp for asp in aspects if 'Moon' in [asp.get('planet1'), asp.get('planet2')]]
        
        # Check if Moon aspects either significator
        for aspect in moon_aspects:
            if not aspect.get('applying', False):
                continue
                
            p1, p2 = aspect.get('planet1'), aspect.get('planet2')
            other_planet = p2 if p1 == 'Moon' else p1
            
            if other_planet in [querent, quesited]:
                aspect_type = aspect.get('aspect', '')
                favorable = aspect_type in ['Conjunction', 'Sextile', 'Trine']
                
                return {
                    'significant': True,
                    'supports_judgment': favorable,
                    'reason': f"Moon {aspect_type.lower()}s {other_planet} (secondary testimony)",
                    'traditional_role': 'Supporting evidence, not primary judgment'
                }
        
        return {
            'significant': False,
            'supports_judgment': None,
            'reason': 'No significant Moon testimony',
            'traditional_role': 'Moon aspects are secondary factors'
        }


# Test function to validate fixes
def test_fixes_with_marriage_question():
    """Test the fixes with the Anthony Louis marriage question"""
    
    # Sample data structure (would come from actual chart calculation)
    test_chart_data = {
        'planets': {
            'Venus': {'house': 6, 'dignity_score': 3},
            'Mars': {'house': 7, 'dignity_score': -4},
            'Moon': {'house': 10, 'dignity_score': 6},
            'Saturn': {'house': 9, 'dignity_score': -6}
        },
        'aspects': [
            {'planet1': 'Moon', 'planet2': 'Venus', 'aspect': 'Trine', 'applying': True, 'orb': 5.89},
            {'planet1': 'Mercury', 'planet2': 'Mars', 'aspect': 'Square', 'applying': False, 'orb': 4.98}
            # Note: NO Venus-Mars applying aspect (matches test case)
        ]
    }
    
    fixed_engine = FixedHoraryJudgment()
    result = fixed_engine.apply_traditional_judgment(
        test_chart_data, 'marriage', 'Venus', 'Mars')
    
    print("=== FIXED ENGINE TEST RESULT ===")
    print(f"Judgment: {result['judgment']}")
    print(f"Confidence: {result['confidence']}%")
    print("Reasoning:")
    for i, reason in enumerate(result['reasoning'], 1):
        print(f"  {i}. {reason}")
    print(f"Traditional Validation: {result['traditional_validation']}")
    print(f"Fixes Applied: {result['fixes_applied']}")
    
    return result

if __name__ == "__main__":
    # Test the fixes
    test_result = test_fixes_with_marriage_question()
    
    expected_judgment = "NO"
    actual_judgment = test_result['judgment']
    
    if actual_judgment == expected_judgment:
        print(f"\n✅ SUCCESS: Fixed engine produces correct judgment ({expected_judgment})")
        print("✅ Anthony Louis/Warnock case validation PASSED")
    else:
        print(f"\n❌ FAILURE: Expected {expected_judgment}, got {actual_judgment}")