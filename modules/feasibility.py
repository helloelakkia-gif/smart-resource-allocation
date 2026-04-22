import math

def haversine_km(lat1, lon1, lat2, lon2):
    """
    Calculate straight-line distance between two GPS points in kilometres.
    Uses the Haversine formula — accurate enough for city-scale distances.
    """
    R = 6371  # Earth radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)
    return R * 2 * math.asin(math.sqrt(a))

def calculate_feasibility(distance_km, hours_per_week, already_assigned=False):
    """
    Score 0-100: how realistic is it to send this volunteer?

    - Distance score  → closer = better  (up to 50 pts)
    - Availability    → more hours = better (up to 40 pts)
    - Not assigned    → 10 pt bonus
    """
    if already_assigned:
        return 0  # volunteer is busy

    # 0 km → 50 pts,  50+ km → 0 pts
    distance_score  = max(0, 50 - distance_km)
    distance_score  = min(distance_score, 50)

    # 1 hr/week → ~2.5 pts,  16+ hrs/week → 40 pts
    availability_score = min((hours_per_week / 16) * 40, 40)

    free_bonus = 10  # not currently assigned

    total = distance_score + availability_score + free_bonus
    return round(min(total, 100), 1)

def get_feasibility_label(score):
    if score >= 70: return "✅ Very Feasible"
    if score >= 40: return "🟡 Feasible"
    if score > 0:   return "⚠️ Low Feasibility"
    return "❌ Unavailable"