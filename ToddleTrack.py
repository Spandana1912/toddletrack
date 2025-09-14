import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# ------------------- Firebase Setup -------------------
if not firebase_admin._apps:
    cred = credentials.Certificate(
    "C:\\Users\\spand\\OneDrive\\Documents\\toddletrack\\toddletrack\\firebase_config.json"
)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ------------------- Streamlit Page Config -------------------
st.set_page_config(page_title="Toddle Track - Parent Dashboard", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        .main {
            background-color: #0e1117;
            color: white;
        }
        .stTextInput>div>div>input, .stTextArea textarea {
            background-color: #1a1c23;
            color: white;
        }
        .stButton>button {
            background-color: #ff4b4b;
            color: white;
            border-radius: 8px;
        }
        .alert-box {
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 10px;
            font-weight: bold;
        }
        .alert-danger {
            background-color: #ff4b4b;
            color: white;
        }
        .alert-warning {
            background-color: #f39c12;
            color: black;
        }
        .alert-success {
            background-color: #2ecc71;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------- Guardian Info -------------------
st.sidebar.title("👨‍👩‍👧 Guardian Info")

guardian_name = st.sidebar.text_input("Guardian Name", "John Doe")
guardian_phone = st.sidebar.text_input("Phone", "+91-9999999999")
guardian_email = st.sidebar.text_input("Email", "parent@example.com")
guardian_address = st.sidebar.text_area("Address", "Amrita Vishwa Vidyapeetham, Coimbatore")

if st.sidebar.button("Update Info"):
    st.sidebar.success("Guardian Info Updated ✅")

# ------------------- Dashboard Header -------------------
st.title("👶 Toddle Track - Parent Dashboard")
st.caption("Real-time child safety monitoring with motion alerts, location tracking & geofencing")

st.markdown("---")

# ------------------- Fetch Child Data -------------------
def fetch_child_data():
    try:
        # Assuming your ESP32 sends data with 'latitude' and 'longitude' fields
        docs = db.collection("child_data").order_by("Time", direction=firestore.Query.DESCENDING).limit(20).stream()
        records = []
        for doc in docs:
            d = doc.to_dict()
            records.append(d)
        if records:
            df = pd.DataFrame(records)
            # Rename columns to match st.map requirements
            df = df.rename(columns={"latitude": "lat", "longitude": "lon"})
            return df
        else:
            return pd.DataFrame(columns=["lat", "lon", "Event", "Time"])
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame(columns=["lat", "lon", "Event", "Time"])

data = fetch_child_data()

# ------------------- Child Location Map -------------------
st.subheader("📍 Child Location")
st.info("Showing latest detected positions of your child on map.")

if not data.empty and "lat" in data.columns and "lon" in data.columns:
    st.map(data[["lat", "lon"]], zoom=15)
else:
    st.warning("No location data available yet.")

# ------------------- Alerts Section -------------------
st.subheader("🚨 Alerts")
if not data.empty:
    latest_events = data.head(5)
    for _, row in latest_events.iterrows():
        event = row.get("Event", "Unknown")
        time = row.get("Time", "Unknown")
        
        if "freefall" in event.lower() or "jerk" in event.lower() or "dash" in event.lower():
            st.markdown(f"<div class='alert-box alert-danger'>⚠️ {event} at {time}</div>", unsafe_allow_html=True)
        elif "geofence" in event.lower():
            st.markdown(f"<div class='alert-box alert-warning'>📍 {event} at {time}</div>", unsafe_allow_html=True)
        elif "sos" in event.lower() or "button" in event.lower():
            st.markdown(f"<div class='alert-box alert-danger'>🚨 SOS Alert: {event} at {time}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='alert-box alert-success'>✅ {event} at {time}</div>", unsafe_allow_html=True)
else:
    st.info("No alerts yet. Your child is safe ✅")
