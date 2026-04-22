import pandas as pd
from modules.feasibility import haversine_km, calculate_feasibility

def match_volunteers(need_row, volunteers_df):
    """
    Return volunteers sorted by combined score:
        combined = urgency_score * 0.5 + feasibility_score * 0.5
    Only returns volunteers whose skills match the need.
    """
    results = []

    for _, vol in volunteers_df.iterrows():

        # ── Skill check ───────────────────────────────────────────
        vol_skills = str(vol.get("skills", "")).lower()
        need_cat   = str(need_row.get("category", "")).lower()
        if need_cat not in vol_skills and "general" not in vol_skills:
            continue

        # ── Already assigned? ─────────────────────────────────────
        already_assigned = (
            str(vol.get("assigned_to", "")).strip() not in ["", "nan"]
        )

        # ── Distance ──────────────────────────────────────────────
        try:
            dist = haversine_km(
                float(need_row["lat"]),  float(need_row["lon"]),
                float(vol["lat"]),       float(vol["lon"])
            )
        except Exception:
            dist = 999

        # ── Feasibility score ─────────────────────────────────────
        feasibility = calculate_feasibility(
            dist,
            float(vol.get("hours_per_week", 1)),
            already_assigned
        )

        urgency = float(need_row.get("urgency_score", 50))

        # ── Combined score ────────────────────────────────────────
        combined = round(urgency * 0.5 + feasibility * 0.5, 1)

        results.append({
            "name":        vol["name"],
            "skills":      vol["skills"],
            "area":        vol["area"],
            "distance_km": round(dist, 1),
            "feasibility": feasibility,
            "combined":    combined,
            "assigned":    already_assigned,
            "vol_id":      vol["id"],
        })

    # Sort best match first
    results.sort(key=lambda x: x["combined"], reverse=True)
    return results