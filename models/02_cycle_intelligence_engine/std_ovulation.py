from std_config import DEFAULT_LUTEAL_PHASE

def estimate_ovulation(predicted_cycle_length: int) -> int:
    """
    Estimates the ovulation day based on the predicted cycle length.
    Typically, the luteal phase (from ovulation to next period) is 14 days.
    """
    
    # Ensure ovulation day makes sense (e.g., if cycle length is abnormally short)
    ovulation_day = predicted_cycle_length - DEFAULT_LUTEAL_PHASE
    
    # Minimum reasonable ovulation day
    if ovulation_day < 8:
        ovulation_day = 8
        
    return ovulation_day
