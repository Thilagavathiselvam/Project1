import streamlit as st
import datetime
import base64
import json
import os

def heart_disease_predict_page():
    st.set_page_config(page_title="Heart Disease Prediction", page_icon="❤️", layout="centered")
    st.title("💓 Heart Disease Prediction Dashboard")

    # --- Animated Heart Image ---
    st.markdown("""
    <style>
        @keyframes heartbeat {
            0% { transform: scale(1); }
            25% { transform: scale(1.1); }
            50% { transform: scale(1); }
            75% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        .heart-container {
            display: flex;
            justify-content: center;
            margin-bottom: 15px;
            animation: heartbeat 1.8s infinite;
        }
    </style>
    <div class="heart-container">
        <img src="https://cdn.pixabay.com/photo/2017/02/23/13/05/heart-2092484_1280.png" width="180">
    </div>
    """, unsafe_allow_html=True)

    # --- Patient Info ---
    st.header("🧍 Patient Details")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        age = st.number_input("Age", 1, 120, 25)
        gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
        email = st.text_input("Email")
    with col2:
        phone = st.text_input("Phone Number")
        address = st.text_area("Address")
        upload_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- Health Parameters ---
    st.header("🩺 Health Parameters")
    c1, c2, c3 = st.columns(3)
    with c1:
        bp = st.number_input("Blood Pressure (mm Hg)", 60, 250, 120)
        cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, 200)
        blood_sugar = st.number_input("Fasting Blood Sugar (mg/dL)", 50, 400, 100)
    with c2:
        heart_rate = st.number_input("Heart Rate (bpm)", 40, 220, 80)
        bmi = st.number_input("Body Mass Index (BMI)", 10.0, 60.0, 22.5, step=0.1)
        ecg = st.selectbox("Resting ECG Result", ["Normal", "ST-T Abnormality", "LVH"])
    with c3:
        smoking = st.selectbox("Smoking Habit", ["No", "Occasionally", "Regularly"])
        alcohol = st.selectbox("Alcohol Intake", ["No", "Occasionally", "Frequently"])
        physical_activity = st.selectbox("Physical Activity", ["Low", "Moderate", "High"])

    # --- Upload Image (ECG/Report/Scan) ---
    st.subheader("🖼️ Upload Report or ECG Image (Optional)")
    uploaded_image = st.file_uploader("Upload JPG or PNG", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Medical Report", width=300)

    # --- Predict Button ---
    if st.button("🔍 Predict Heart Disease"):
        if not name or gender == "Select" or not email:
            st.warning("⚠️ Please fill all mandatory fields (Name, Gender, Email).")
        else:
            # --- Simple Logic for Demonstration ---
            risk_score = 0
            if bp > 140: risk_score += 1
            if cholesterol > 240: risk_score += 1
            if blood_sugar > 120: risk_score += 1
            if bmi > 30: risk_score += 1
            if smoking == "Regularly": risk_score += 1
            if alcohol == "Frequently": risk_score += 1
            if physical_activity == "Low": risk_score += 1

            risk = "⚠️ High Risk" if risk_score >= 3 else "✅ Low Risk"
            color = "red" if "High" in risk else "green"

            st.markdown(f"<h3 style='text-align:center;color:{color};'>{risk}</h3>", unsafe_allow_html=True)
            st.info(f"🕒 Prediction Time: {upload_time}")

            # --- Save Record ---
            record = {
                "name": name,
                "age": age,
                "gender": gender,
                "email": email,
                "phone": phone,
                "address": address,
                "bp": bp,
                "cholesterol": cholesterol,
                "blood_sugar": blood_sugar,
                "heart_rate": heart_rate,
                "bmi": bmi,
                "ecg": ecg,
                "smoking": smoking,
                "alcohol": alcohol,
                "physical_activity": physical_activity,
                "risk": risk,
                "timestamp": upload_time
            }

            if not os.path.exists("records"):
                os.mkdir("records")
            with open(f"records/{name.replace(' ', '_')}.json", "w") as f:
                json.dump(record, f, indent=4)

            # --- Downloadable Text Report ---
            report = f"""
            💓 **Heart Disease Prediction Report**
            ----------------------------------------
            👤 Name: {name}
            🎂 Age: {age}
            🚻 Gender: {gender}
            📧 Email: {email}
            📱 Phone: {phone}
            🏠 Address: {address}
            🕒 Time: {upload_time}

            🩺 Blood Pressure: {bp} mm Hg
            🧈 Cholesterol: {cholesterol} mg/dL
            🍬 Blood Sugar: {blood_sugar} mg/dL
            ❤️ Heart Rate: {heart_rate} bpm
            ⚖️ BMI: {bmi}
            🩻 ECG: {ecg}
            🚬 Smoking: {smoking}
            🍷 Alcohol: {alcohol}
            🏃‍♀️ Activity Level: {physical_activity}

            📊 Risk Prediction: {risk}
            """

            b64 = base64.b64encode(report.encode()).decode()
            href = f'<a href="data:file/txt;base64,{b64}" download="{name}_Heart_Report.txt">📥 Download Report</a>'
            st.markdown(href, unsafe_allow_html=True)

            st.success("✅ Record saved successfully!")

    # --- View Saved Records ---
    st.divider()
    st.subheader("📂 View Saved Patient Records")
    if os.path.exists("records"):
        files = os.listdir("records")
        if files:
            selected = st.selectbox("Select a record to view:", files)
            with open(f"records/{selected}", "r") as f:
                data = json.load(f)
            st.json(data)
        else:
            st.info("No patient records found yet.")
