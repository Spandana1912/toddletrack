import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from streamlit_autorefresh import st_autorefresh

# ---------------------------------------------------------------
# 🔐 1. Secure Firebase Setup using Streamlit Secrets
# ---------------------------------------------------------------
try:
    if not firebase_admin._apps:
        # Load credentials securely from Streamlit Secrets
        cred = credentials.Certificate(st.secrets["firebase"])
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://toddletrack-fd848-default-rtdb.asia-southeast1.firebasedatabase.app/"
        })
except Exception as e:
    st.error("❌ Firebase initialization failed.")
    st.stop()

# ---------------------------------------------------------------
# 🧭 2. Streamlit Page Configuration
# ---------------------------------------------------------------
st.set_page_config(page_title="Toddle Track - Motion Monitor", layout="centered")
st.title("🚼 Toddle Track - Motion Monitoring Dashboard")

# ---------------------------------------------------------------
# 👨‍👩‍👧 3. Guardian Info Sidebar
# ---------------------------------------------------------------
st.sidebar.title("👨‍👩‍👧 Guardian Info")

guardian_name = st.sidebar.text_input("Guardian Name", "John Doe")
guardian_phone = st.sidebar.text_input("Phone", "+91-9999999999")
guardian_email = st.sidebar.text_input("Email", "parent@example.com")
guardian_address = st.sidebar.text_area("Address", "Amrita Vishwa Vidyapeetham, Coimbatore")

if st.sidebar.button("Update Info"):
    st.sidebar.success("Guardian Info Updated ✅")

# ---------------------------------------------------------------
# 🔁 4. Auto Refresh Configuration
# ---------------------------------------------------------------
refresh_rate = st.sidebar.slider("Auto-refresh rate (seconds)", 2, 15, 5)
st_autorefresh(interval=refresh_rate * 1000, key="firebase_refresh")

# ---------------------------------------------------------------
# 🔎 5. Fetch Latest Sensor Data from Firebase Realtime DB
# ---------------------------------------------------------------
@st.cache_data(ttl=10)
def fetch_sensor_data():
    """Fetch latest sensor data from Firebase."""
    try:
        ref = db.reference("sensor/current")
        data = ref.get()
        return data
    except Exception as e:
        st.error(f"⚠️ Error fetching data from Firebase: {e}")
        return None

data = fetch_sensor_data()

# ---------------------------------------------------------------
# 📊 6. Display Motion Data
# ---------------------------------------------------------------
if data:
    prediction = data.get("prediction", "Unknown")
    ax = data.get("ax", 0.0)
    ay = data.get("ay", 0.0)
    az = data.get("az", 0.0)

    st.subheader("📊 Latest Sensor Data")
    st.write(f"**Prediction:** {prediction}")
    st.write(f"**Acceleration (m/s²):**  X = {ax:.2f},  Y = {ay:.2f},  Z = {az:.2f}")

    # -----------------------------------------------------------
    # 🚨 7. Motion Alert Logic
    # -----------------------------------------------------------
    abnormal_states = ["jerk", "shake", "freefall"]

    if prediction.lower() in abnormal_states:
        st.error("🚨 ALERT: Sudden or dangerous motion detected!")
        st.warning("⚠ Please check on the child immediately.")
    elif prediction.lower() == "no abnormal motion":
        st.info("✅ All clear — No abnormal motion detected.")
    else:
        st.info("⚙ Monitoring in progress...")
else:
    st.warning("⏳ Waiting for sensor data... Ensure ESP32 is sending updates to Firebase.")

# ---------------------------------------------------------------
# 🧾 8. Footer
# ---------------------------------------------------------------
st.caption("👶 Developed by Hack 'n Chill 😎❄ — ToddleTrack © 2025")
