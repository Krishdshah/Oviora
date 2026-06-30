from typing import Dict, Any, List

from std_validators import validate_cycle_request
from std_predictor import predict_cycle_length
from std_cycle_day import calculate_cycle_day
from std_ovulation import estimate_ovulation
from std_phase import determine_phase
from std_hormones import estimate_hormones
from std_response_builder import build_response

def predict(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main orchestrator for the Cycle Intelligence Engine.
    """
    
    # 1. Extract inputs
    last_period_start_date = payload.get("last_period_start_date")
    age = payload.get("age", 25)
    height = payload.get("height", 165.0)
    weight = payload.get("weight", 65.0)
    bmi = payload.get("bmi", 23.9)
    previous_cycle_lengths = payload.get("previous_cycle_lengths", [])
    
    # 2. Validation
    validate_cycle_request(last_period_start_date, age, bmi, previous_cycle_lengths)
    
    # 3. Predict Cycle Length (ML)
    predicted_cycle_length = predict_cycle_length(age, height, weight, bmi, previous_cycle_lengths)
    
    # 4. Calculate Current Cycle Day
    cycle_day = calculate_cycle_day(last_period_start_date)
    
    # 5. Estimate Ovulation Day
    ovulation_day = estimate_ovulation(predicted_cycle_length)
    
    # 6. Determine Phase
    phase = determine_phase(cycle_day, ovulation_day)
    
    # 7. Estimate Hormones
    hormones = estimate_hormones(cycle_day, ovulation_day, predicted_cycle_length)
    
    # 8. Build and Return Response
    return build_response(
        cycle_day=cycle_day,
        phase=phase,
        predicted_cycle_length=predicted_cycle_length,
        predicted_ovulation_day=ovulation_day,
        hormones=hormones,
        previous_cycle_lengths=previous_cycle_lengths
    )
