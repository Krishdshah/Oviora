from datetime import datetime, date
from typing import List, Optional

def validate_cycle_request(
    last_period_start_date: str,
    age: int,
    bmi: float,
    previous_cycle_lengths: List[int]
) -> None:
    # 1. Last period date cannot be in the future
    try:
        parsed_date = datetime.strptime(last_period_start_date, "%Y-%m-%d").date()
        if parsed_date > date.today():
            raise ValueError("last_period_start_date cannot be in the future.")
    except ValueError as e:
        if "time data" in str(e):
            raise ValueError("Invalid date format. Expected YYYY-MM-DD.")
        else:
            raise e
            
    # 2. Age between 12-60
    if not (12 <= age <= 60):
        raise ValueError("Age must be between 12 and 60.")
        
    # 3. BMI > 0
    if bmi <= 0:
        raise ValueError("BMI must be greater than 0.")
        
    # 4. Previous cycle list not empty
    if not previous_cycle_lengths:
        raise ValueError("previous_cycle_lengths cannot be empty.")
        
    # 5. Cycle length between 15-60 days
    for length in previous_cycle_lengths:
        if not (15 <= length <= 60):
            raise ValueError(f"Invalid cycle length {length}. Must be between 15 and 60 days.")
            
    return True
