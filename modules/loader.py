import pandas as pd
import os

NEEDS_FILE      = "data/needs.csv"
VOLUNTEERS_FILE = "data/volunteers.csv"
UPLOADS_DIR     = "data/uploads"

def ensure_dirs():
    """Create folders if they don't exist."""
    os.makedirs("data",       exist_ok=True)
    os.makedirs(UPLOADS_DIR,  exist_ok=True)

def load_needs():
    if os.path.exists(NEEDS_FILE):
        return pd.read_csv(NEEDS_FILE)
    return pd.DataFrame(columns=[
        "id", "area", "category", "description",
        "people_affected", "days_pending",
        "lat", "lon",
        "proof_file", "urgency_score", "status"
    ])

def save_needs(df):
    df.to_csv(NEEDS_FILE, index=False)

def load_volunteers():
    if os.path.exists(VOLUNTEERS_FILE):
        return pd.read_csv(VOLUNTEERS_FILE)
    return pd.DataFrame(columns=[
        "id", "name", "skills", "area",
        "lat", "lon",
        "hours_per_week", "assigned_to"
    ])

def save_volunteers(df):
    df.to_csv(VOLUNTEERS_FILE, index=False)