import math
from typing import Dict

def estimate_hormones(cycle_day: int, ovulation_day: int, cycle_length: int) -> Dict[str, int]:
    """
    Estimates hormone levels (Estrogen, Progesterone, LH, FSH) on a scale (e.g., relative index or typical pg/mL / mIU/mL).
    Uses a simplified clinical curve approximation relative to the cycle length and ovulation day.
    """
    
    # Base baseline values
    estrogen = 30
    progesterone = 10
    lh = 5
    fsh = 5
    
    # Normalize day relative to ovulation (- means before, + means after)
    days_from_ovulation = cycle_day - ovulation_day
    
    # 1. Estrogen (Peaks right before ovulation, secondary smaller peak in mid-luteal)
    if -7 <= days_from_ovulation <= 0:
        # Rises steeply up to ovulation
        estrogen = 30 + int(70 * math.exp(-0.1 * (days_from_ovulation + 1)**2))
    elif 3 <= days_from_ovulation <= 9:
        # Secondary luteal peak
        estrogen = 40 + int(30 * math.sin(math.pi * (days_from_ovulation - 3) / 6))
        
    # 2. LH (Sharp peak ~24-36 hrs before ovulation)
    if -2 <= days_from_ovulation <= 1:
        # Sharp surge
        lh = 10 + int(65 * math.exp(-0.8 * (days_from_ovulation + 0.5)**2))
        
    # 3. FSH (Slight rise in early follicular, small peak at ovulation)
    if cycle_day <= 5:
        fsh = 8 + (5 - cycle_day)
    elif -2 <= days_from_ovulation <= 1:
        fsh = 5 + int(25 * math.exp(-0.5 * (days_from_ovulation)**2))
        
    # 4. Progesterone (Low until ovulation, then rises significantly in luteal phase)
    if days_from_ovulation > 0:
        # Parabolic shape in luteal phase, peaking around mid-luteal
        luteal_duration = cycle_length - ovulation_day
        if luteal_duration > 0 and days_from_ovulation < luteal_duration:
            mid_luteal = luteal_duration / 2
            progesterone = 10 + int(60 * (1 - ((days_from_ovulation - mid_luteal) / mid_luteal)**2))
        if progesterone < 10:
            progesterone = 10

    return {
        "estrogen": max(20, estrogen),
        "progesterone": max(5, progesterone),
        "lh": max(5, lh),
        "fsh": max(4, fsh)
    }
