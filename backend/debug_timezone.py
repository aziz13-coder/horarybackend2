#!/usr/bin/env python3
"""
Debug script to trace the exact timezone conversion issue
"""

import datetime
import pytz
from timezonefinder import TimezoneFinder

def debug_timezone_conversion():
    """Debug the exact conversion process"""
    
    print("=== DEBUGGING TIMEZONE CONVERSION ===")
    
    # Your exact inputs
    date_str = "02/03/2004"  # March 2, 2004 (DD/MM/YYYY)
    time_str = "22:00"       # 10 PM
    timezone_str = "America/New_York"  # EST/EDT
    
    # Washington DC coordinates (from geocoding)
    lat = 38.8950
    lon = -77.0365
    
    print(f"Input: {date_str} {time_str} {timezone_str}")
    print(f"Coordinates: {lat}, {lon}")
    
    # Step 1: Parse the datetime
    print("\n--- STEP 1: Parse datetime ---")
    try:
        dt_naive = datetime.datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
        print(f"Parsed naive datetime: {dt_naive}")
        print(f"This represents: {dt_naive.strftime('%A, %B %d, %Y at %I:%M %p')}")
    except Exception as e:
        print(f"Parse error: {e}")
        return
    
    # Step 2: Get timezone from coordinates
    print("\n--- STEP 2: Check timezone from coordinates ---")
    tf = TimezoneFinder()
    coord_timezone = tf.timezone_at(lat=lat, lng=lon)
    print(f"Timezone from coordinates: {coord_timezone}")
    
    # Step 3: Apply timezone
    print(f"\n--- STEP 3: Apply timezone '{timezone_str}' ---")
    try:
        tz = pytz.timezone(timezone_str)
        print(f"Timezone object: {tz}")
        
        # Check if this time exists in March 2004 (DST transition?)
        dt_local = tz.localize(dt_naive)
        print(f"Localized datetime: {dt_local}")
        print(f"UTC offset: {dt_local.utcoffset()}")
        
        # Convert to UTC
        dt_utc = dt_local.astimezone(pytz.UTC)
        print(f"UTC datetime: {dt_utc}")
        
        # Convert back to local time for display
        display_local = dt_utc.astimezone(tz)
        print(f"Back to local: {display_local}")
        
        # What would this look like in a different timezone?
        print("\n--- Checking other timezone representations ---")
        est_tz = pytz.timezone('EST')
        est_time = dt_utc.astimezone(est_tz)
        print(f"In EST timezone: {est_time}")
        
        # Check system local time representation
        import time
        local_tz = pytz.timezone('UTC')  # Or get system timezone
        try:
            # Get system timezone
            local_tz_name = time.tzname[0]
            print(f"System timezone: {local_tz_name}")
        except:
            print("Could not determine system timezone")
            
    except Exception as e:
        print(f"Timezone error: {e}")
    
    # Step 4: Check for DST transitions around this date
    print(f"\n--- STEP 4: Check DST transitions in March 2004 ---")
    march_dates = [
        datetime.datetime(2004, 3, 1, 22, 0),   # March 1
        datetime.datetime(2004, 3, 2, 22, 0),   # March 2 (your date)
        datetime.datetime(2004, 3, 14, 22, 0),  # March 14 (typical DST start)
        datetime.datetime(2004, 3, 15, 22, 0),  # March 15
    ]
    
    for dt in march_dates:
        try:
            dt_with_tz = tz.localize(dt)
            print(f"{dt.date()}: {dt_with_tz} (offset: {dt_with_tz.utcoffset()})")
        except pytz.NonExistentTimeError:
            print(f"{dt.date()}: NON-EXISTENT TIME (DST spring forward)")
        except pytz.AmbiguousTimeError:
            print(f"{dt.date()}: AMBIGUOUS TIME (DST fall back)")

def debug_result_format():
    """Debug what could produce the result format you saw"""
    
    print(f"\n=== DEBUGGING RESULT FORMAT ===")
    
    # Your result: "Local Time: 04/02/2004, 5:00:00"
    # This looks like February 4, 2004 at 5:00 AM
    
    result_dt = datetime.datetime(2004, 2, 4, 5, 0, 0)
    print(f"Result datetime: {result_dt}")
    print(f"Formatted as: {result_dt.strftime('%d/%m/%Y, %H:%M:%S')}")
    
    # How far off is this from your intended time?
    intended_dt = datetime.datetime(2004, 3, 2, 22, 0, 0)
    diff = result_dt - intended_dt
    print(f"Difference: {diff}")
    print(f"That's {abs(diff.days)} days and {abs(diff.seconds)//3600} hours off")
    
    # Could this be a UTC conversion error?
    print(f"\n--- Checking UTC conversion scenarios ---")
    
    # If March 2, 2004 10 PM EST was treated as UTC
    intended_utc = datetime.datetime(2004, 3, 2, 22, 0, 0)  # Treated as UTC
    intended_utc = intended_utc.replace(tzinfo=pytz.UTC)
    
    # Convert to different timezones
    timezones_to_check = [
        'America/New_York',
        'Europe/London', 
        'Asia/Tokyo',
        'UTC'
    ]
    
    for tz_name in timezones_to_check:
        tz = pytz.timezone(tz_name) if tz_name != 'UTC' else pytz.UTC
        local_time = intended_utc.astimezone(tz)
        print(f"{tz_name}: {local_time}")

if __name__ == "__main__":
    debug_timezone_conversion()
    debug_result_format()