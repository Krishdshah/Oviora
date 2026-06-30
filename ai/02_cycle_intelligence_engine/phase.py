from .config import MENSTRUAL_DAYS, OVULATION_WINDOW

def determine_phase(cycle_day: int, ovulation_day: int) -> str:
    """
    Determines the cycle phase based on cycle day and ovulation day.
    """
    
    if cycle_day <= MENSTRUAL_DAYS:
        return "Menstrual"
        
    ovulation_start = ovulation_day - OVULATION_WINDOW
    ovulation_end = ovulation_day + OVULATION_WINDOW
    
    if cycle_day < ovulation_start:
        return "Follicular"
        
    if cycle_day <= ovulation_end:
        return "Ovulatory"
        
    return "Luteal"
