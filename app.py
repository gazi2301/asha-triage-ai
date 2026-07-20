import streamlit as st
from backend import analyze_patient

# 1. Set up high-contrast, mobile-friendly tablet configuration
st.set_page_config(page_title="ASHA Triage AI", layout="centered")

st.title("🏥 Frontline Health Triage Terminal")
st.markdown("---")

st.subheader("📋 Enter Patient Vitals & Information")

# 2. Design input fields with large fonts/controls for field usability
age = st.number_input("Patient Age", min_value=0, max_value=120, value=30, step=1)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])

st.markdown("### Vitals Monitoring")
spo2 = st.slider("Blood Oxygen Saturation (SpO2 %)", min_value=50, max_value=100, value=98, help="Critical below 90%")
pulse = st.slider("Pulse Rate (Heartbeats per Minute)", min_value=30, max_value=200, value=75)

st.markdown("### Symptoms")
symptoms = st.text_area("Describe Symptoms / Primary Complaints", placeholder="Example: Severe chest pain, sweating, high fever for 3 days...")

st.markdown("---")

# 3. Trigger button to execute analysis
if st.button("🚨 RUN EMERGENCY TRIAGE ANALYSIS", use_container_width=True):
    if not symptoms.strip():
        st.warning("⚠️ Please provide at least one symptom description before running triage.")
    else:
        with st.spinner("Analyzing patient metrics using clinical triage protocols..."):
            
            # Format input data to match what the backend expects
            formatted_input = f"Age: {age}, Gender: {gender}, SpO2: {spo2}%, Pulse: {pulse} bpm, Symptoms: {symptoms}"
            
            # Send to your operational Gemini backend
            result = analyze_patient(formatted_input)
            
            st.markdown("### 📋 AI Evaluation & Routing Decision")
            
            if "error" in result:
                st.error(f"System Error: {result['error']}")
            else:
                triage = result.get("triage_level", "GREEN").upper()
                action = result.get("action_plan", "No immediate high-risk indicators found.")
                
                # Render color-coded visual alerts based on the JSON level returned
                if triage == "RED":
                    st.error(f"🔴 TRIAGE STATUS: {triage} (EMERGENCY)")
                    st.markdown(f"**CRITICAL INSTRUCTION:** {action}")
                elif triage == "YELLOW":
                    st.warning(f"🟡 TRIAGE STATUS: {triage} (OBSERVATION)")
                    st.markdown(f"**CLINICAL INSTRUCTION:** {action}")
                else:
                    st.success(f"🟢 TRIAGE STATUS: {triage} (STABLE)")
                    st.markdown(f"**ROUTINE INSTRUCTION:** {action}")
