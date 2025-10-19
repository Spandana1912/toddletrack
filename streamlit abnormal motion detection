import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from streamlit_autorefresh import st_autorefresh

# ------------------- Firebase Setup -------------------
if not firebase_admin._apps:
    cred = credentials.Certificate(r"C:\Hackathon\AIOT\FIREBASE_GPS\serviceAccountKey.json.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://toddletrack-fd848-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# ------------------- Streamlit Setup -------------------
st.set_page_config(page_title="Toddle Track - Motion Monitor", layout="centered")
st.title("🚼 Toddle Track - Motion Monitoring Dashboard")

# ------------------- Sidebar: Guardian Info -------------------
st.sidebar.title("👨‍👩‍👧 Guardian Info")
guardian_name = st.sidebar.text_input("Guardian Name", "John Doe")
guardian_phone = st.sidebar.text_input("Phone", "+91-9999999999")
guardian_email = st.sidebar.text_input("Email", "parent@example.com")
guardian_address = st.sidebar.text_area("Address", "Amrita Vishwa Vidyapeetham, Coimbatore")

if st.sidebar.button("Update Info"):
    st.sidebar.success("Guardian Info Updated ✅")

# ------------------- Refresh Rate -------------------
refresh_rate = st.sidebar.slider("Auto-refresh rate (seconds)", 2, 15, 5)
st_autorefresh(interval=refresh_rate * 1000, key="firebase_refresh")

# ------------------- Fetch Data -------------------
def fetch_sensor_data():
    try:
        ref = db.reference("sensor/current")
        return ref.get()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# ------------------- Display Data -------------------
data = fetch_sensor_data()

if data:
    prediction = data.get("prediction", "Unknown")
    ax = data.get("ax", 0)
    ay = data.get("ay", 0)
    az = data.get("az", 0)

    st.subheader("📊 Latest Sensor Data")
    st.write(f"*Prediction:* {prediction}")
    st.write(f"*Acceleration (m/s²):* X={ax:.2f}, Y={ay:.2f}, Z={az:.2f}")

    # ------------------- Alert Logic -------------------
    if prediction.lower() in ["jerk", "shake", "freefall"]:
        st.error("🚨 ALERT: Child might be in danger! Sudden motion detected!")
        st.warning("Please check on the child immediately.")
    elif prediction.lower() == "no abnormal motion":
        st.info("✅ All clear: No abnormal motion detected.")
    else:
        st.info("⚙ Monitoring...")

else:
    st.warning("Waiting for sensor data... (Ensure ESP32 is sending to Firebase)")

# ------------------- Footer -------------------
st.caption("Developed by Hack 'n Chill😎❄ -ToddleTrack 👶")
