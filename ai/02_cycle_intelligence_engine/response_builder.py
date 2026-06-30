from typing import Dict, Any, List
import numpy as np
from .config import ENGINE_VERSION, MODEL_VERSION

def build_response(
    cycle_day: int,
    phase: str,
    predicted_cycle_length: int,
    predicted_ovulation_day: int,
    hormones: Dict[str, int],
    previous_cycle_lengths: List[int]
) -> Dict[str, Any]:
    """
    Builds the final JSON payload expected by the frontend.
    """
    
    # 1. Calculate derived fields
    days_until_next_period = predicted_cycle_length - cycle_day
    if days_until_next_period < 0:
        days_until_next_period = 0
        
    fertile_window_start = max(1, predicted_ovulation_day - 4)
    fertile_window_end = predicted_ovulation_day + 1
    
    # 2. Confidence Score (based on cycle regularity)
    # If standard deviation is high, confidence is lower. Max 95, min 50.
    if len(previous_cycle_lengths) >= 2:
        std_dev = np.std(previous_cycle_lengths)
        confidence = max(50, min(95, int(95 - (std_dev * 5))))
    else:
        confidence = 75 # default for low data
        
    # 3. Phase Reason
    if phase == "Menstrual":
        phase_reason = f"Cycle Day {cycle_day} falls within the typical menstrual period (Days 1-5)."
    elif phase == "Follicular":
        phase_reason = f"Cycle Day {cycle_day} is after menstruation but before the estimated ovulation window (Day {fertile_window_start})."
    elif phase == "Ovulatory":
        phase_reason = f"Cycle Day {cycle_day} is within the estimated ovulation window (Days {fertile_window_start}-{fertile_window_end})."
    else:
        phase_reason = f"Cycle Day {cycle_day} is past ovulation (Day {predicted_ovulation_day}), entering the Luteal phase."
        
    # 4. Recommendation Context
    recommendation_context = {
        "high_energy_day": phase in ["Follicular", "Ovulatory"],
        "strength_training": phase in ["Follicular", "Ovulatory"],
        "hydration_priority": phase == "Menstrual",
        "iron_focus": phase == "Menstrual"
    }
    
    return {
        "cycle_day": cycle_day,
        "phase": phase,
        "phase_reason": phase_reason,
        "days_until_next_period": days_until_next_period,
        "predicted_cycle_length": predicted_cycle_length,
        "predicted_ovulation_day": predicted_ovulation_day,
        "fertile_window": {
            "start": fertile_window_start,
            "end": fertile_window_end
        },
        "hormones": hormones,
        "confidence": confidence,
        "recommendation_context": recommendation_context,
        "engine_version": ENGINE_VERSION,
        "model_version": MODEL_VERSION
    }
