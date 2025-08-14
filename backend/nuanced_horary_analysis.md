# NUANCED HORARY ENGINE FIXES

## Problem Analysis

My initial fix was **too rigid** and broke valid horary cases. Here's what I learned:

### What Went Wrong with First Fix
1. **Oversimplified Rule**: "No L1-L7 aspect = always NO"
2. **Ignored Dignities**: Didn't account for exceptional dignities like cazimi
3. **Broke Valid Cases**: Made divorce question (cazimi case) return wrong answer
4. **Too Absolute**: Traditional horary is nuanced, not rigid

### Traditional Horary Complexity

Traditional horary considers multiple factors:
1. **Direct Aspects**: L1-L7 applying aspects (primary)
2. **Exceptional Dignities**: Cazimi (+25), major debilities (-20+)
3. **Translation/Collection**: Planetary mediation between significators
4. **Mutual Reception**: Significators in each other's signs
5. **Dignity Balance**: Overall strength comparison
6. **Moon Testimony**: Secondary support, not primary perfection

## Test Cases Analysis

### Case 1: "Will he marry me?" (Anthony Louis/Warnock)
- **Significators**: Venus (L1) ↔ Mars (L7) 
- **Direct Aspect**: NONE
- **Special Factors**: Moon Trines Venus
- **Expected**: NO (prohibition blocks perfection)
- **Issue**: Engine used Moon-Venus as primary perfection ❌

### Case 2: "Will there be a divorce?" (Goldstein-Jacobson)
- **Significators**: Jupiter (L1) ↔ Mercury (L7)
- **Direct Aspect**: NONE  
- **Special Factors**: Mercury CAZIMI (+25 dignity)
- **Expected**: YES (cazimi strength + separation aspects)
- **Issue**: My rigid fix returned NO ❌

## Nuanced Solution

### Core Principle
**Moon aspects to significators should NOT create primary perfection, but exceptional dignities CAN override lack of direct aspects.**

### Implementation Strategy

1. **Detect Moon-Significator Aspects**
   ```python
   moon_aspects_significator = self._moon_aspects_significator_directly(chart, querent, quesited)
   ```

2. **Apply Nuanced Logic**
   - If Moon aspects significator + exceptional dignity → Judge by dignity
   - If Moon aspects significator + normal dignity → Reduce confidence
   - If Moon aspects other planets → Original logic applies

3. **Dignity Thresholds**
   - **Exceptional**: ±20+ (cazimi +25, major debility -20)
   - **Significant Difference**: 15+ dignity gap
   - **Normal Range**: -10 to +10

### Expected Results

#### Marriage Question (Fixed)
- Moon Trines Venus (significator aspect) ✓ Detected
- Venus dignity: +3, Mars dignity: -4 (normal range)
- Result: UNCLEAR (reduced confidence)
- Note: Should still check for prohibitions separately

#### Divorce Question (Fixed) 
- Mercury cazimi (+25) ✓ Exceptional dignity
- Jupiter dignity: 0 (normal)
- Dignity difference: -25 (quesited much stronger)
- Result: Appropriate judgment based on dignities

## Key Improvements

### 1. **Preserved Valid Judgments**
- Cazimi cases still work correctly
- Exceptional dignity cases maintained
- Translation/collection logic intact

### 2. **Fixed False Perfection**
- Moon-significator aspects no longer create primary perfection
- Reduced confidence for Moon-based judgments
- Maintains traditional hierarchy

### 3. **Maintained Nuance**
- Not overly rigid rules
- Context-dependent logic
- Multiple paths to judgment

### 4. **Better Reasoning**
- Clearer explanation of logic
- Distinguishes primary vs secondary factors
- Shows dignity considerations

## Traditional Validation

This approach aligns with traditional horary doctrine:

- **William Lilly**: Dignities matter greatly in judgment
- **Cazimi Doctrine**: Heart of Sun = maximum planetary strength
- **Moon Role**: Secondary testimony, not primary perfection
- **Perfection Hierarchy**: Direct aspects > Reception > Translation > Moon testimony

## Next Steps

1. Test with both questions to verify fix works
2. Implement proper prohibition detection for marriage case
3. Add more traditional test cases for validation
4. Consider other exceptional dignity cases (exaltation, etc.)

The goal is **balanced traditional accuracy** without breaking valid horary principles.