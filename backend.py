import streamlit as st
from google import genai
# ... your other imports ...

# Get the key from the Streamlit cloud secrets
api_key = st.secrets["API_KEY"]
client = genai.Client(api_key=api_key)

def analyze_patient(patient_data):
    system_prompt = """
    You are an expert Clinical Triage AI assistant for rural Indian ASHA workers. 
    Categorize the urgency based on vitals and symptoms.
    
    - RED (Emergency): SpO2 below 90, severe chest pain, unconsciousness, or pulse > 120. Refer to District Hospital.
    - YELLOW (Observation): SpO2 90-94, high fever, or moderate pain. Treat at Primary Health Centre (PHC).
    - GREEN (Stable): Normal vitals, minor symptoms. Treat at home or local clinic.
    
    You MUST respond ONLY with a raw JSON object. Format exactly like this:
    {"triage_level": "RED", "action_plan": "Your strict instruction here"}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{system_prompt}\n\nPatient Data: {patient_data}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1
            )
        )
        
        result = json.loads(response.text)
        return result
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("Testing the Modern GenAI Triage Logic...\n")
    dummy_patient = "Age: 45, Gender: Male, SpO2: 88%, Pulse: 110, Symptoms: Complaining of heavy chest pain."
    print(f"Input Data: {dummy_patient}\n")
    analysis = analyze_patient(dummy_patient)
    print("AI Decision Output:")
    print(json.dumps(analysis, indent=4))
