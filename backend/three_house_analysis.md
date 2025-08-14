# Three-House Handling Analysis: Horary Engine Capabilities

## **Current State: PARTIAL SUPPORT** ❌

Based on comprehensive codebase analysis, the horary engine has **limited capability** for handling questions requiring 3 houses.

---

## **What Works ✅**

### **1. Question Analysis Layer**
The engine **CAN** identify and return 3 houses:

```python
# Examples from codebase:
return {"type": "money", "houses": [1, 7, 8]}  # Husband's possessions  
return {"type": "money", "houses": [1, 4, 5]}  # Father's possessions
return {"type": "money", "houses": [1, 10, 11]} # Mother's possessions
```

### **2. House Derivation System**
Traditional house-from-house calculations work correctly:
- **Husband's possessions**: 7th house (husband) + 2nd house = 8th house 
- **Father's possessions**: 4th house (father) + 2nd house = 5th house
- **Mother's possessions**: 10th house (mother) + 2nd house = 11th house

---

## **Critical Limitation ❌**

### **Significator Assignment Bottleneck**

The engine has a **fundamental limitation** in the `_determine_significators()` method:

```python
def _determine_significators(self, houses: List[int], question_type: str) -> Dict[str, Any]:
    significators = {
        "querent_house": 1,  # Always 1st house
        "quesited_house": houses[1] if len(houses) > 1 else 7,  # ❌ ONLY USES houses[1]
        # ...
    }
```

**Problem**: Even when 3 houses are identified `[1, 7, 8]`, only `houses[1]` (7th house) is used as the quesited house, **ignoring the actual target house** (8th house).

---

## **Impact on Judgment Logic ❌**

### **Example: "Will my husband sell his car?"**

**Correct Traditional Analysis**:
- Houses: [1, 7, 8] (querent, husband, husband's possessions)
- Significators: Saturn (L1) and **Mercury (L8)** 
- Question about: **Car sale** (8th house matter)

**Current Engine Logic**:
- Houses: [1, 7, 8] ✅ (correctly identified)
- Significators: Saturn (L1) and **Moon (L7)** ❌ (wrong significator)
- Question analyzed as: **Husband relationship** (7th house matter)

**Result**: Engine uses wrong significator and misinterprets the question type.

---

## **Specific Limitations**

### **1. Single Quesited Significator**
- Engine expects **binary relationship**: Querent vs. Quesited
- Cannot handle **tertiary relationships**: Querent → Person → Person's Possession
- **Missing logic** for multi-significator analysis

### **2. Aspect Analysis Bottleneck**
```python
def _identify_significators(self, chart: HoraryChart, question_analysis: Dict):
    querent_house = 1
    quesited_house = question_analysis["significators"]["quesited_house"]  # Only 1 house
    # No logic for analyzing multiple target houses
```

### **3. Perfection Logic Limitation**
```python
def _check_enhanced_perfection(self, chart: HoraryChart, querent: Planet, quesited: Planet):
    # Only checks aspects between 2 planets
    # No logic for A→B→C or A→(B+C) relationships
```

---

## **Traditional Horary Requirements for 3-House Questions**

### **Scenarios Requiring 3+ Houses:**

1. **Derived Houses**: "Will my husband sell his car?" (1st, 7th, 8th)
2. **Third Party Questions**: "Will my friend get the job?" (1st, 11th, 10th)  
3. **Complex Relationships**: "Will my daughter marry her boyfriend?" (1st, 5th, 7th from 5th)
4. **Conditional Questions**: "Should I buy this house for my mother?" (1st, 4th, 10th)

### **Traditional Analysis Methods:**

1. **Multiple Significators**: May require analyzing L1, L7, L8 simultaneously
2. **Sequential Perfection**: L8 applies to L1, or L1 translates between L7 and L8
3. **Tertiary Reception**: Mutual reception between any of the 3 significators
4. **House Strength Analysis**: Compare dignity of all relevant house rulers

---

## **Required Improvements**

### **1. Enhanced Significator Logic**
```python
def _determine_significators_enhanced(self, houses: List[int], question_type: str):
    significators = {
        "querent_house": 1,
        "quesited_house": houses[-1],  # Use LAST house (actual target)
        "intermediate_houses": houses[1:-1] if len(houses) > 2 else [],
        "all_relevant_houses": houses
    }
```

### **2. Multi-Significator Perfection**
```python
def _check_multi_house_perfection(self, chart: HoraryChart, houses: List[int]):
    # Check direct perfection between L1 and final target
    # Check translation through intermediate houses  
    # Check collection involving multiple significators
    # Analyze reception between all relevant rulers
```

### **3. Tertiary Relationship Logic**
```python
def _analyze_derived_house_questions(self, chart: HoraryChart, houses: List[int]):
    # Traditional rule: Question about X's Y uses house of X + derived house of Y
    # Example: Husband's money = 7th house + 2nd house = 8th house
    # Must analyze both the person AND the derived matter
```

---

## **Current Workarounds**

### **Manual House Override**
The engine supports manual house specification:
```python
# User can manually specify: "1,8" to force correct significators
manual_houses = [1, 8]  # Bypasses automatic 3-house detection
```

### **Question Rewording**
- Instead: "Will my husband sell his car?" 
- Reword: "Will the car be sold?" (focuses on 2nd house possessions)

---

## **Conclusion**

**Answer: NO** - The engine cannot properly handle 3-house questions.

**Current Capability**: 
- ✅ Can identify 3 houses  
- ❌ Cannot use all 3 houses in judgment
- ❌ Limited to 2-significator analysis
- ❌ Misses traditional derived house logic

**Impact**: 
- **False negatives** for valid traditional horary questions
- **Incorrect significator assignment** for complex relationships  
- **Reduced accuracy** for family/possession/third-party questions

**Recommendation**: 
Implement enhanced multi-house logic to handle traditional horary's full scope of question types.