from datetime import datetime, date

def calculate_cycle_day(last_period_start_date: str) -> int:
    """
    Calculates the current cycle day based on the last period start date.
    Cycle day 1 is the first day of the period.
    """
    try:
        start_date = datetime.strptime(last_period_start_date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Expected YYYY-MM-DD.")
        
    today = date.today()
    delta = today - start_date
    
    # Cycle day is 1-indexed (day 1 is the day it started)
    cycle_day = delta.days + 1
    
    if cycle_day < 1:
        raise ValueError("Last period start date cannot be in the future.")
        
    return cycle_day
