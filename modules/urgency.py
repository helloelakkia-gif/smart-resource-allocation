def calculate_urgency(people_affected, days_pending, category):
    """
    Calculate urgency score based on:
    - number of people affected
    - how long request is pending
    - type of request
    """

    score = 0

    # People affected weight
    if people_affected > 50:
        score += 3
    elif people_affected > 20:
        score += 2
    else:
        score += 1

    # Days pending weight
    if days_pending > 5:
        score += 3
    elif days_pending > 2:
        score += 2
    else:
        score += 1

    # Category weight
    if category == "medical":
        score += 3
    elif category == "food":
        score += 2
    else:
        score += 1

    return score


def get_urgency_label(score):
    if score >= 7:
        return "High"
    elif score >= 4:
        return "Medium"
    else:
        return "Low"
    