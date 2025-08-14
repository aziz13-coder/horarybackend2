#!/usr/bin/env python3
"""
Debug question classification for "Will she go out with me?"
"""

def debug_question_classification():
    question = "Will she go out with me?"
    question_lower = question.lower()
    
    # Simulate the question_patterns from the engine
    question_patterns = {
        'love': ['love', 'romance', 'romantic', 'crush', 'attraction', 'affection'],
        'relationship': ['relationship', 'partner', 'boyfriend', 'girlfriend', 'spouse', 'husband', 'wife', 'dating', 'together'],
        'marriage': ['marry', 'marriage', 'wedding', 'engagement', 'engaged', 'propose', 'proposal'],
        'partnership': ['partnership', 'business partner', 'collaborate', 'joint venture'],
        'divorce': ['divorce', 'separation', 'separate', 'split up', 'break up'],
        'career': ['career', 'promotion', 'advancement', 'professional'],
        'job': ['job', 'work', 'employment', 'position', 'hire', 'fired', 'quit'],
        'business': ['business', 'company', 'enterprise', 'startup', 'venture'],
        'money': ['money', 'cash', 'income', 'salary', 'wage', 'pay', 'payment'],
        'wealth': ['wealth', 'rich', 'fortune', 'prosperity', 'financial success'],
        'financial': ['financial', 'finance', 'budget', 'debt', 'loan', 'credit', 'investment'],
        'health': ['health', 'healthy', 'wellness', 'medical condition', 'recovery'],
        'illness': ['ill', 'sick', 'disease', 'condition', 'symptoms', 'diagnosis'],
        'medical': ['medical', 'doctor', 'hospital', 'treatment', 'medicine', 'therapy'],
        'travel': ['travel', 'trip', 'journey', 'vacation', 'holiday', 'abroad'],
        'journey': ['journey', 'voyage', 'expedition', 'pilgrimage'],
        'education': ['education', 'school', 'university', 'college', 'degree', 'academic', 'study', 'learn', 'exam', 'test', 'grade', 'pass', 'fail', 'student', 'teacher', 'professor', 'class', 'course', 'semester', 'graduation', 'graduate', 'diploma', 'certificate', 'tutored', 'tutor', 'finals', 'midterm', 'paralegal'],
        'legal': ['legal', 'law', 'court', 'judge', 'lawyer', 'attorney', 'litigation', 'trial'],
        'lawsuit': ['lawsuit', 'sue', 'legal action', 'court case', 'litigation', 'plaintiff', 'defendant'],
        'court': ['court', 'courtroom', 'hearing', 'trial', 'judicial'],
        'property': ['property', 'real estate', 'house', 'apartment', 'home', 'buy', 'sell', 'rent'],
        'home': ['home', 'house', 'residence', 'dwelling', 'household'],
        'family': ['family', 'relatives', 'parents', 'siblings', 'children', 'mother', 'father'],
        'children': ['children', 'child', 'kids', 'son', 'daughter', 'baby', 'pregnancy', 'pregnant'],
        'pregnancy': ['pregnancy', 'pregnant', 'expecting', 'baby', 'conception', 'birth'],
        'death': ['death', 'die', 'deceased', 'funeral', 'mortality'],
        'inheritance': ['inheritance', 'inherit', 'legacy', 'will', 'estate', 'bequest'],
        'lost_object': ['lost', 'missing', 'find', 'locate', 'misplaced', 'stolen'],
        'missing_person': ['missing person', 'disappeared', 'whereabouts', 'location of']
    }
    
    print(f"Question: '{question}'")
    print(f"Lowercased: '{question_lower}'")
    print()
    
    # Check what patterns match
    matches = []
    for pattern_type, keywords in question_patterns.items():
        for keyword in keywords:
            if keyword in question_lower:
                matches.append((pattern_type, keyword))
                break
    
    print("Pattern matches found:")
    if matches:
        for pattern_type, keyword in matches:
            print(f"  - {pattern_type}: matched '{keyword}'")
    else:
        print("  - No matches found")
        
    # The issue: "go out" should be relationship/dating context
    print()
    print("Issue analysis:")
    print("'go out with me' is clearly a relationship/dating question")
    print("But 'go out' is not in the relationship keywords list!")
    print()
    
    # What should happen
    print("Missing keywords in 'relationship' category:")
    missing_keywords = ['go out', 'date', 'go on a date', 'ask out', 'see each other']
    for keyword in missing_keywords:
        print(f"  - '{keyword}' (would match: {'go out' in question_lower})")
    
    # House assignments  
    house_assignments = {
        'love': {'querent_house': 1, 'quesited_house': 7},
        'relationship': {'querent_house': 1, 'quesited_house': 7},
        'general': {'querent_house': 1, 'quesited_house': 7}
    }
    
    print()
    print("Current result:")
    if matches:
        first_match = matches[0][0]
        assignment = house_assignments.get(first_match, {'querent_house': 1, 'quesited_house': 7})
        print(f"  - Classification: {first_match}")
        print(f"  - House assignment: {assignment}")
    else:
        print(f"  - Classification: general (fallback)")
        print(f"  - House assignment: {house_assignments['general']}")
        
    print()
    print("But based on JSON output, it used 8th house - why?")

if __name__ == "__main__":
    debug_question_classification()