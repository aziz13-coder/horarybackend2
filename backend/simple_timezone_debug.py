#!/usr/bin/env python3
"""
Simple timezone debug without external dependencies
"""

import datetime

def debug_conversion():
    print("=== TIMEZONE CONVERSION DEBUG ===")
    
    # Your input
    date_str = "02/03/2004"  # March 2, 2004
    time_str = "22:00"       # 10 PM
    
    print(f"Input: {date_str} {time_str}")
    
    # Parse the date
    dt_naive = datetime.datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
    print(f"Parsed: {dt_naive}")
    print(f"This is: {dt_naive.strftime('%A, %B %d, %Y at %I:%M %p')}")
    
    # Your result
    print(f"\n--- YOUR RESULT ---")
    result = "04/02/2004, 5:00:00"  
    result_dt = datetime.datetime.strptime(result, "%d/%m/%Y, %H:%M:%S")
    print(f"Result datetime: {result_dt}")
    print(f"This is: {result_dt.strftime('%A, %B %d, %Y at %I:%M %p')}")
    
    # Calculate the difference
    diff = result_dt - dt_naive
    print(f"\nDifference: {diff}")
    print(f"Days difference: {diff.days}")
    print(f"Hours difference: {diff.seconds // 3600}")
    print(f"Total hours: {diff.total_seconds() / 3600}")
    
    # This is very suspicious - let's see what could cause this
    print(f"\n--- ANALYSIS ---")
    
    # Could it be month confusion?
    february_4 = datetime.datetime(2004, 2, 4, 5, 0)  # Feb 4
    march_2 = datetime.datetime(2004, 3, 2, 22, 0)    # Mar 2
    
    print(f"February 4, 2004 5 AM: {february_4}")
    print(f"March 2, 2004 10 PM: {march_2}")
    
    diff2 = february_4 - march_2
    print(f"Difference: {diff2}")
    print(f"That's {abs(diff2.total_seconds() / 3600)} hours earlier")
    
    # Could it be a timezone arithmetic error?
    print(f"\n--- TIMEZONE ARITHMETIC ERRORS ---")
    
    # If someone subtracted too many hours
    original_time = march_2
    
    # EST is UTC-5, but what if the system subtracted more?
    for hours_subtracted in range(1, 30):
        test_result = original_time - datetime.timedelta(hours=hours_subtracted)
        if test_result.day == 4 and test_result.month == 2 and test_result.hour == 5:
            print(f"FOUND: Subtracting {hours_subtracted} hours gives {test_result}")
            print(f"This suggests an error of {hours_subtracted - 5} extra hours")
    
    # Could it be date format confusion + timezone error?
    print(f"\n--- DATE FORMAT + TIMEZONE ERRORS ---")
    
    # What if "03/02/2004" was interpreted as "03/02" = February 3rd?
    feb_3 = datetime.datetime(2004, 2, 3, 22, 0)  # February 3, 2004 10 PM
    print(f"If interpreted as Feb 3: {feb_3}")
    
    # Then what timezone conversion would give Feb 4, 5 AM?
    target = datetime.datetime(2004, 2, 4, 5, 0)
    hours_diff = (target - feb_3).total_seconds() / 3600
    print(f"Feb 3 10 PM -> Feb 4 5 AM = {hours_diff} hours forward")
    print("This suggests adding 7 hours (like going from UTC-7 to UTC)")

if __name__ == "__main__":
    debug_conversion()