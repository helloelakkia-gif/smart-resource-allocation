def calculate_urgency(people_affected, days_pending, category,
                       has_proof=False, distance_km=None):
    """
    Score 0-100 based on:
    - People affected     → up to 40 pts
    - Days pending        → up to 25 pts
    - Category severity   → up to 20 pts
    - Proof uploaded      → up to 10 pts bonus
    - Distance penalty    → up to -5 pts if far
    """
    category_weights = {
        "Medical":    20,
        "Food":       18,
        "Shelter":    16,
        "Sanitation": 14,
        "Education":  12,
        "Other":       8,
    }

    people_score       = min((people_affected / 500) * 40, 40)
    days_score         = min((days_pending / 30) * 25, 25)
    cat_score          = category_weights.get(category, 8)
    proof_bonus        = 10 if has_proof else 0

    dist_penalty = 0
    if distance_km is not None:
        dist_penalty = min(distance_km / 100, 5)

    total = people_score + days_score + cat_score + proof_bonus - dist_penalty
    return round(max(0, min(total, 100)), 1)

def get_urgency_label(score):
    if score >= 75: return "🔴 Critical"
    if score >= 50: return "🟠 High"
    if score >= 25: return "🟡 Medium"
    return "🟢 Low"