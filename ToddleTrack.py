import streamlit as st
import pandas as pd
from datetime import datetime
from math import radians, cos, sin, sqrt, atan2

# ===============================
# Page Config
# ===============================
st.set_page_config(page_title="Toddle Track Dashboard", layout="wide")

# ===============================
# Header
# ===============================
st.markdown(
    """
    <h1 style="text-align:center; color:#2C3E50;">
        👶 Toddle Track - Parent Dashboard
    </h1>
    <p style="text-align:center; color:#7F8C8D;">
        Real-time child safety monitoring with motion alerts, location tracking & geofencing
    </p>
    <hr style="border:1px solid #BDC3C7;">
    """,
    unsafe_allow_html=True
)

# ===============================
# Guardian Info Section (Sidebar)
# ===============================
st.sidebar.header("👨‍👩‍👧 Guardian Info")
guardian_name = st.sidebar.text_input("Guardian Name", "John Doe")
guardian_phone = st.sidebar.text_input("Phone", "+91-9999999999")
guardian_email = st.sidebar.text_input("Email", "parent@example.com")
guardian_address = st.sidebar.text_area("Address", "123, MG Road, Bangalore")

if st.sidebar.button("Update Info"):
    st.sidebar.success("✅ Guardian info updated!")

# ===============================
# Dummy Child Data (replace with Firebase later)
# ===============================
data = pd.DataFrame([
    {"Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
     "Event": "Freefall detected",
     "Lat": 10.9032, "Lon": 76.9020},  # Near Amrita CBE
    {"Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
     "Event": "Normal activity",
     "Lat": 10.9055, "Lon": 76.8980}   # Another nearby point
])

# ===============================
# Layout with 2 Columns
# ===============================
col1, col2 = st.columns([2, 1])

# ----------- Child Location Map -----------
with col1:
    st.markdown("### 📍 Child Location")
    st.info("Showing latest detected positions of your child on map.")
    map_data = data.rename(columns={"Lat": "lat", "Lon": "lon"})
    st.map(map_data[["lat", "lon"]], zoom=15)

# ----------- Alerts (Styled Cards on Right Side) -----------
with col2:
    st.markdown("### 🚨 Alerts")
    for i, row in data.iterrows():
        if row["Event"] != "Normal activity":
            # Alert events
            st.markdown(
                f"""
                <div style="padding:15px; margin-bottom:12px; background-color:#FDEDEC; 
                            border-left: 6px solid #C0392B; border-radius:10px;">
                    <b style="color:#C0392B; font-size:16px;">⚠️ {row['Event']}</b><br>
                    <span style="color:#922B21;">🕒 {row['Time']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            # Normal activity
            st.markdown(
                f"""
                <div style="padding:15px; margin-bottom:12px; background-color:#E8F8F5; 
                            border-left: 6px solid #1E8449; border-radius:10px;">
                    <b style="color:#1E8449; font-size:16px;">✅ {row['Event']}</b><br>
                    <span style="color:#196F3D;">🕒 {row['Time']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
