from typing import Dict, Any

def build_response(
    cycle_day: int,
    phase: str,
    predicted_cycle_length: int,
    predicted_ovulation_day: int,
    hormones: Dict[str, int]
) -> Dict[str, Any]:
    """
    Builds the final JSON payload expected by the frontend.
    """
    
    # Calculate derived fields
    days_until_next_period = predicted_cycle_length - cycle_day
    if days_until_next_period < 0:
        days_until_next_period = 0
        
    fertile_window_start = max(1, predicted_ovulation_day - 4)
    fertile_window_end = predicted_ovulation_day + 1
    
    # Base confidence score (can be adjusted based on variance in previous cycles)
    confidence = 90 
    
    return {
        "cycle_day": cycle_day,
        "phase": phase,
        "days_until_next_period": days_until_next_period,
        "predicted_cycle_length": predicted_cycle_length,
        "predicted_ovulation_day": predicted_ovulation_day,
        "fertile_window": {
            "start": fertile_window_start,
            "end": fertile_window_end
        },
        "hormones": hormones,
        "confidence": confidence
    }
