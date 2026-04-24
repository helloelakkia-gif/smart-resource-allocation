# ─────────────────────────────────────────────────────────────────────────────
#  Smart Resource Allocation System — Upgraded Hackathon Edition
#  Run:  python -m streamlit run app.py
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st
import pandas as pd
import plotly.express as px
import uuid, os
from PIL import Image
from geopy.geocoders import Nominatim

from modules.loader      import (load_needs, save_needs,
                                  load_volunteers, save_volunteers,
                                  ensure_dirs, UPLOADS_DIR)
from modules.urgency     import calculate_urgency, get_urgency_label
from modules.feasibility import haversine_km, get_feasibility_label
from modules.matcher     import match_volunteers

# ── Bootstrap ─────────────────────────────────────────────────────────────────
ensure_dirs()
st.set_page_config(
    page_title="Smart Resource Allocation",
    page_icon="🤝",
    layout="wide"
)

# ── Global CSS — clean look ───────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        border-left: 4px solid #4f8bf9;
    }
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #1a1a2e;
    }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
# ── Geocoder helper ───────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def get_coordinates(address):
    """Convert city/address text to lat/lon using free OpenStreetMap API."""
    try:
        geolocator = Nominatim(user_agent="smart_resource_app")
        location   = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
    except Exception:
        pass
    return None, None

# ── Geocoder helper ───────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def get_coordinates(address):
    """Convert city/address text to lat/lon using free OpenStreetMap API."""
    try:
        geolocator = Nominatim(user_agent="smart_resource_app")
        location   = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
    except Exception:
        pass
    return None, None

# ── Geocoder helper ───────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def get_coordinates(address):
    """Convert city/address text to lat/lon using free OpenStreetMap API."""
    try:
        geolocator = Nominatim(user_agent="smart_resource_app")
        location   = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
    except Exception:
        pass
    return None, None

# ── Geocoder helper ───────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def get_coordinates(address):
    """Convert city/address text to lat/lon using free OpenStreetMap API."""
    try:
        geolocator = Nominatim(user_agent="smart_resource_app")
        location   = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
    except Exception:
        pass
    return None, None

# ── Geocoder helper ───────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def get_coordinates(address):
    """Convert city/address text to lat/lon using free OpenStreetMap API."""
    try:
        geolocator = Nominatim(user_agent="smart_resource_app")
        location   = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
    except Exception:
        pass
    return None, None

# ── Geocoder helper ───────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def get_coordinates(address):
    """Convert city/address text to lat/lon using free OpenStreetMap API."""
    try:
        geolocator = Nominatim(user_agent="smart_resource_app")
        location   = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
    except Exception:
        pass
    return None, None

needs_df      = load_needs()
volunteers_df = load_volunteers()

# Fix column types to prevent dtype errors
if not volunteers_df.empty:
    volunteers_df["assigned_to"] = volunteers_df["assigned_to"].astype(str).replace("nan", "")
    volunteers_df["id"] = volunteers_df["id"].astype(str)
if not needs_df.empty:
    needs_df["id"] = needs_df["id"].astype(str)
    needs_df["status"] = needs_df["status"].astype(str)

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.image(
    "https://img.icons8.com/fluency/96/helping-hand.png", width=60
)
st.sidebar.title("Smart Resource Allocation")
st.sidebar.caption("")

page = st.sidebar.radio("Navigate", [
    "📊 Dashboard",
    "➕ Report a Need",
    "🙋 Register Volunteer",
    "🔗 Match Volunteers",
    "📥 Upload CSV",
])

st.sidebar.divider()
st.sidebar.metric("Total Needs",      len(needs_df))
st.sidebar.metric("Total Volunteers", len(volunteers_df))

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 ── DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 Dashboard":
    st.title("📊 Community Needs Dashboard")

    if needs_df.empty:
        st.info("No data yet. Go to **Report a Need** to get started.")
        st.stop()

    # ── Summary row ───────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Needs",      len(needs_df))
    c2.metric("Critical 🔴",
              len(needs_df[needs_df["urgency_score"] >= 75])
              if "urgency_score" in needs_df.columns else 0)
    c3.metric("Volunteers",       len(volunteers_df))
    c4.metric("Open Needs",
              len(needs_df[needs_df["status"] == "Open"])
              if "status" in needs_df.columns else 0)

    st.divider()

    # ── Map ───────────────────────────────────────────────────────────────────
    st.subheader("🗺️ Live Map — Needs & Volunteers")

    map_rows = []

    if "lat" in needs_df.columns:
        for _, r in needs_df.iterrows():
            try:
                map_rows.append({
                    "lat":   float(r["lat"]),
                    "lon":   float(r["lon"]),
                    "type":  "Need",
                    "label": f"{r['category']} — {r['area']}",
                    "score": float(r.get("urgency_score", 50)),
                })
            except Exception:
                pass

    if "lat" in volunteers_df.columns:
        for _, r in volunteers_df.iterrows():
            try:
                map_rows.append({
                    "lat":   float(r["lat"]),
                    "lon":   float(r["lon"]),
                    "type":  "Volunteer",
                    "label": r["name"],
                    "score": 50,
                })
            except Exception:
                pass

    if map_rows:
        map_df = pd.DataFrame(map_rows)
        fig_map = px.scatter_mapbox(
            map_df,
            lat="lat", lon="lon",
            color="type",
            size="score",
            hover_name="label",
            color_discrete_map={"Need": "#e74c3c", "Volunteer": "#2ecc71"},
            zoom=9,
            center={"lat": map_df["lat"].mean(), "lon": map_df["lon"].mean()},
            height=500,
            mapbox_style="open-street-map",
            size_max=25,
        )
        fig_map.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(
                orientation="h",
                yanchor="bottom", y=1.02,
                xanchor="right",  x=1,
                font=dict(size=14)
            )
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        import plotly.graph_objects as go
        fig_empty = go.Figure(go.Scattermapbox())
        fig_empty.update_layout(
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=13.0827, lon=80.2707),
                zoom=9,
            ),
            height=420,
            margin=dict(l=0, r=0, t=0, b=0),
        )
        st.plotly_chart(fig_empty, use_container_width=True)
        st.caption("📍 Showing Chennai by default — add needs/volunteers to see markers.")

    st.divider()

    # ── Charts ────────────────────────────────────────────────────────────────
    col_l, col_r = st.columns(2)

    with col_l:
        st.subheader("Urgency by Area")
        if "urgency_score" in needs_df.columns:
            area_df = (needs_df.groupby("area")["urgency_score"]
                       .mean().reset_index())
            fig = px.bar(
                area_df, x="area", y="urgency_score",
                color="urgency_score",
                color_continuous_scale=["#2ecc71","#f39c12","#e74c3c"],
                range_color=[0, 100],
                labels={"urgency_score": "Avg Urgency", "area": "Area"}
            )
            fig.update_layout(height=280, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.subheader("Urgency Distribution")
        if "urgency_score" in needs_df.columns:
            fig2 = px.histogram(
                needs_df, x="urgency_score", nbins=10,
                color_discrete_sequence=["#4f8bf9"],
                labels={"urgency_score": "Urgency Score"}
            )
            fig2.update_layout(height=280)
            st.plotly_chart(fig2, use_container_width=True)

    # ── Ranked table ──────────────────────────────────────────────────────────
    st.subheader("All Needs — Ranked by Urgency")
    if "urgency_score" in needs_df.columns:
        display = needs_df.copy()
        display["label"] = display["urgency_score"].apply(get_urgency_label)
        display = display.sort_values("urgency_score", ascending=False)
        st.dataframe(
            display[["area","category","description",
                      "people_affected","days_pending",
                      "urgency_score","label","status"]],
            use_container_width=True
        )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 ── REPORT A NEED
# ══════════════════════════════════════════════════════════════════════════════
elif page == "➕ Report a Need":
    st.title("➕ Report a Community Need")

    with st.form("need_form", clear_on_submit=True):
        st.subheader("📋 Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            area     = st.text_input("Area / Locality",
                                      placeholder="e.g. North Zone, Ward 5")
            category = st.selectbox("Category",
                ["Medical","Food","Shelter","Education","Sanitation","Other"])
            people   = st.number_input("People affected",  min_value=1, value=50)
            days     = st.number_input("Days pending",     min_value=0, value=1)

        with col2:
            description = st.text_area("Description", height=120,
                placeholder="Describe the need clearly...")
            location_input = st.text_input(
                "📍 Location (city or address)",
                placeholder="e.g. Chennai, Anna Nagar, Delhi"
            )

        st.subheader("📸 Upload Proof (optional — boosts urgency score)")
        proof_file = st.file_uploader(
            "Upload image or video as proof",
            type=["jpg","jpeg","png","mp4","mov"]
        )

        # Preview
        if proof_file and proof_file.type.startswith("image"):
            st.image(Image.open(proof_file), caption="Preview", width=300)
            proof_file.seek(0)   # reset pointer after preview

        submitted = st.form_submit_button("🚀 Submit Need", type="primary")

    if submitted:
        if not area or not description:
            st.error("Please fill in Area and Description.")
        else:
            # ── Save uploaded file ─────────────────────────────────────────
            proof_filename = ""
            if proof_file:
                proof_filename = f"{uuid.uuid4().hex[:8]}_{proof_file.name}"
                save_path = os.path.join(UPLOADS_DIR, proof_filename)
                with open(save_path, "wb") as f:
                    f.write(proof_file.read())

            # ── Calculate urgency ──────────────────────────────────────────
            # Auto-convert address to coordinates
            lat, lon = get_coordinates(location_input if location_input else area)
            if lat is None:
                lat, lon = 13.0827, 80.2707  # fallback to Chennai

            score = calculate_urgency(
                people, days, category,
                has_proof=(proof_filename != "")
            )

            new_row = {
                "id":              str(uuid.uuid4())[:8],
                "area":            area,
                "category":        category,
                "description":     description,
                "people_affected": people,
                "days_pending":    days,
                "lat":             lat,
                "lon":             lon,
                "proof_file":      proof_filename,
                "urgency_score":   score,
                "status":          "Open",
            }
            needs_df = pd.concat(
                [needs_df, pd.DataFrame([new_row])], ignore_index=True
            )
            save_needs(needs_df)

            st.success(
                f"✅ Need submitted!  "
                f"Urgency Score: **{score}/100** — {get_urgency_label(score)}"
            )
            if proof_filename:
                st.info("📎 Proof uploaded — urgency score boosted by +10 pts")
            st.balloons()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 ── REGISTER VOLUNTEER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🙋 Register Volunteer":
    st.title("🙋 Volunteer Registration")

    with st.form("vol_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name   = st.text_input("Full Name")
            skills = st.multiselect("Skills", [
                "Medical","Food","Shelter","Education",
                "Sanitation","General","Transport","Counseling"
            ])
            area  = st.text_input("Your Area",
                placeholder="e.g. North Zone  (or 'Flexible')")
            hours = st.slider("Hours available per week", 1, 40, 5)

        with col2:
            st.write("📍 Your Location")
            location_input = st.text_input(
                "City or Address",
                placeholder="e.g. Chennai, Velachery, Mumbai"
            )

        submitted = st.form_submit_button("✅ Register", type="primary")

    if submitted:
        if not name or not skills or not area:
            st.error("Please fill in all fields.")
        else:
            lat, lon = get_coordinates(location_input if location_input else area)
            if lat is None:
                lat, lon = 13.0827, 80.2707  # fallback to Chennai

            new_vol = {
                "id":           str(uuid.uuid4())[:8],
                "name":         name,
                "skills":       ", ".join(skills),
                "area":         area,
                "lat":          lat,
                "lon":          lon,
                "hours_per_week": hours,
                "assigned_to":  "",
            }
            volunteers_df = pd.concat(
                [volunteers_df, pd.DataFrame([new_vol])], ignore_index=True
            )
            save_volunteers(volunteers_df)
            st.success(f"Welcome, {name}! You are now registered 🎉")

    if not volunteers_df.empty:
        st.subheader("Registered Volunteers")
        st.dataframe(
            volunteers_df[["name","skills","area","hours_per_week"]],
            use_container_width=True
        )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 ── MATCH VOLUNTEERS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔗 Match Volunteers":
    st.title("🔗 Smart Volunteer Matching")
    st.caption("Ranked by: Urgency × 0.5  +  Feasibility × 0.5  +  Distance")

    if needs_df.empty or volunteers_df.empty:
        st.warning("Add at least one need and one volunteer first.")
        st.stop()

    open_needs = needs_df[needs_df["status"] == "Open"].sort_values(
        "urgency_score", ascending=False
    )

    if open_needs.empty:
        st.success("All needs have been assigned! 🎉")
        st.stop()

    for _, need in open_needs.iterrows():
        label = (f"{get_urgency_label(need['urgency_score'])}  |  "
                 f"{need['area']} — {need['category']}  "
                 f"(Score: {need['urgency_score']})")

        with st.expander(label):
            col1, col2, col3 = st.columns(3)
            col1.metric("People Affected", int(need["people_affected"]))
            col2.metric("Days Pending",    int(need["days_pending"]))
            col3.metric("Urgency Score",   need["urgency_score"])

            st.write(f"**Description:** {need['description']}")

            # Show proof image if exists
            if str(need.get("proof_file","")).strip() not in ["","nan"]:
                proof_path = os.path.join(UPLOADS_DIR, need["proof_file"])
                if os.path.exists(proof_path) and need["proof_file"].lower().endswith(
                    ("jpg","jpeg","png")
                ):
                    st.image(proof_path, caption="Submitted proof", width=260)

            # ── Run matching ───────────────────────────────────────────────
            matches = match_volunteers(need, volunteers_df)

            if not matches:
                st.warning("No matching volunteers found for this need.")
            else:
                st.subheader(f"🎯 {len(matches)} Volunteer(s) Found")

                match_df = pd.DataFrame(matches)
                match_df["feasibility_label"] = match_df["feasibility"].apply(
                    get_feasibility_label
                )
                st.dataframe(
                    match_df[[
                        "name","skills","area",
                        "distance_km","feasibility",
                        "feasibility_label","combined"
                    ]],
                    use_container_width=True
                )

                best = matches[0]
                st.info(
                    f"🏆 Best match: **{best['name']}**  |  "
                    f"Distance: {best['distance_km']} km  |  "
                    f"Combined Score: {best['combined']}"
                )

                if st.button(f"✅ Assign {best['name']}", key=str(need["id"])):
                    needs_df.loc[
                        needs_df["id"] == need["id"], "status"
                    ] = f"Assigned to {best['name']}"
                    volunteers_df.loc[
                        volunteers_df["id"] == best["vol_id"], "assigned_to"
                    ] = need["id"]
                    save_needs(needs_df)
                    save_volunteers(volunteers_df)
                    st.success(f"🎉 {best['name']} assigned successfully!")
                    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 ── UPLOAD CSV
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📥 Upload CSV":
    st.title("📥 Bulk Upload via CSV")

    # ── Needs upload ──────────────────────────────────────────────────────────
    st.subheader("Upload Community Needs")
    st.caption("Required columns: area, category, description, "
               "people_affected, days_pending, lat, lon")

    up_needs = st.file_uploader("Needs CSV", type="csv", key="up_needs")
    if up_needs:
        new_data = pd.read_csv(up_needs)
        new_data["urgency_score"] = new_data.apply(
            lambda r: calculate_urgency(
                r["people_affected"], r["days_pending"], r["category"]
            ), axis=1
        )
        new_data["status"]     = "Open"
        new_data["proof_file"] = ""
        new_data["id"]         = [str(uuid.uuid4())[:8] for _ in range(len(new_data))]

        needs_df = pd.concat([needs_df, new_data], ignore_index=True)
        save_needs(needs_df)
        st.success(f"✅ {len(new_data)} needs imported and scored!")
        st.dataframe(new_data, use_container_width=True)

    st.divider()

    # ── Volunteers upload ─────────────────────────────────────────────────────
    st.subheader("Upload Volunteers")
    st.caption("Required columns: name, skills, area, "
               "hours_per_week, lat, lon")

    up_vols = st.file_uploader("Volunteers CSV", type="csv", key="up_vols")
    if up_vols:
        new_vols = pd.read_csv(up_vols)
        new_vols["assigned_to"] = ""
        new_vols["id"]          = [str(uuid.uuid4())[:8] for _ in range(len(new_vols))]
        volunteers_df = pd.concat([volunteers_df, new_vols], ignore_index=True)
        save_volunteers(volunteers_df)
        st.success(f"✅ {len(new_vols)} volunteers imported!")
        st.dataframe(new_vols, use_container_width=True)

    # ── CSV templates ─────────────────────────────────────────────────────────
    st.divider()
    st.subheader("📄 Download Sample CSV Templates")

    sample_needs = pd.DataFrame([{
        "area":"North Zone","category":"Medical",
        "description":"Need doctor","people_affected":200,
        "days_pending":10,"lat":13.0827,"lon":80.2707
    }])
    sample_vols = pd.DataFrame([{
        "name":"Dr. Priya","skills":"Medical",
        "area":"North Zone","hours_per_week":10,
        "lat":13.0900,"lon":80.2800
    }])

    col1, col2 = st.columns(2)
    col1.download_button(
        "⬇️ Sample Needs CSV",
        sample_needs.to_csv(index=False),
        "sample_needs.csv", "text/csv"
    )
    col2.download_button(
        "⬇️ Sample Volunteers CSV",
        sample_vols.to_csv(index=False),
        "sample_volunteers.csv", "text/csv"
    )