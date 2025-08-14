#!/usr/bin/env python3
"""
Simple test to debug datetime conversion without external dependencies
"""

import datetime

def test_date_parsing():
    """Test what happens with ambiguous date formats"""
    print("=== TESTING DATE PARSING ISSUE ===")
    
    user_input = "03/02/2004"
    print(f"User input: {user_input}")
    
    # The backend expects YYYY-MM-DD format
    backend_format = "%Y-%m-%d %H:%M"
    print(f"Backend expects: {backend_format}")
    
    # Different interpretations:
    interpretations = [
        ("March 2, 2004 (MM/DD/YYYY)", "2004-03-02"),
        ("February 3, 2004 (DD/MM/YYYY)", "2004-02-03")
    ]
    
    time_str = "22:00"
    
    for desc, iso_date in interpretations:
        print(f"\n--- {desc} ---")
        datetime_str = f"{iso_date} {time_str}"
        print(f"Attempting to parse: {datetime_str}")
        
        try:
            dt = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            print(f"SUCCESS: Parsed as {dt}")
            print(f"Day of year: {dt.timetuple().tm_yday}")
            print(f"Weekday: {dt.strftime('%A')}")
        except Exception as e:
            print(f"ERROR: {e}")
    
    # Test what would happen if input was passed directly
    print(f"\n--- What if '03/02/2004' was passed directly? ---")
    try:
        # This should fail
        dt = datetime.datetime.strptime(f"{user_input} {time_str}", "%Y-%m-%d %H:%M")
        print(f"Somehow succeeded: {dt}")
    except Exception as e:
        print(f"Expected error: {e}")

def test_est_timezone():
    """Test EST timezone issues"""
    print(f"\n=== TESTING EST TIMEZONE ===")
    
    try:
        import pytz
        
        # Test different timezone strings
        timezone_options = [
            "EST",
            "US/Eastern", 
            "America/New_York"
        ]
        
        test_datetime = datetime.datetime(2004, 3, 2, 22, 0)  # March 2, 2004 10 PM
        
        for tz_str in timezone_options:
            print(f"\n--- Testing {tz_str} ---")
            try:
                tz = pytz.timezone(tz_str)
                print(f"Timezone object: {tz}")
                
                # Localize the datetime
                dt_local = tz.localize(test_datetime)
                print(f"Localized: {dt_local}")
                
                # Convert to UTC
                dt_utc = dt_local.astimezone(pytz.UTC)
                print(f"UTC: {dt_utc}")
                
                # What's the UTC offset?
                offset = dt_local.utcoffset()
                print(f"UTC offset: {offset}")
                
            except Exception as e:
                print(f"ERROR with {tz_str}: {e}")
                
    except ImportError:
        print("pytz not available for timezone testing")

def test_result_format():
    """Test what could cause the final result format"""
    print(f"\n=== TESTING RESULT FORMAT ===")
    
    # Your result showed: "2/4/2004, 5:00:00 AM"
    # Let's see what could produce this
    
    possible_dates = [
        datetime.datetime(2004, 2, 4, 5, 0, 0),   # February 4, 2004 5 AM
        datetime.datetime(2004, 4, 2, 5, 0, 0),   # April 2, 2004 5 AM  
    ]
    
    for dt in possible_dates:
        print(f"DateTime: {dt}")
        print(f"Formatted: {dt.strftime('%m/%d/%Y, %I:%M:%S %p')}")
        print(f"ISO format: {dt.isoformat()}")
        
        # How far off is this from the intended time?
        intended = datetime.datetime(2004, 3, 2, 22, 0, 0)  # March 2 10 PM
        diff = dt - intended
        print(f"Difference from intended: {diff}")
        print()

if __name__ == "__main__":
    test_date_parsing()
    test_est_timezone() 
    test_result_format()