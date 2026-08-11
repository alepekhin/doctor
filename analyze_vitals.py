"""Extract and analyze vitals data using Ollama AI."""

import sys
from sqlalchemy import create_engine, text
from ollama import chat

DB_URL = "postgresql://postgres:mysecretpassword@localhost/postgres"
MODEL = "carstenuhlig/omnicoder-2-9b:latest"

def extract_vitals(patient_id=None):
    """Fetch vitals with measurement date from medical_data table."""
    engine = create_engine(DB_URL)
    try:
        with engine.connect() as conn:
            if patient_id:
                print(f"one patient\n")
                query = text(f"""
                    SELECT 
                        id,
                        patient_id,
                        vitals_measurement_date,
                        measurement_source,
                        data->'vitals' as vitals
                    FROM medical_data
                    WHERE patient_id = :patient_id
                    ORDER BY vitals_measurement_date DESC NULLS LAST
                """)
                result = conn.execute(query, {"patient_id": patient_id})
            else:
                result = conn.execute(text("""
                    SELECT 
                        id,
                        patient_id,
                        vitals_measurement_date,
                        measurement_source,
                        data->'vitals' as vitals
                    FROM medical_data
                    ORDER BY vitals_measurement_date DESC NULLS LAST
                """))
            
            vitals_data = []
            for row in result:
                # data is already a dict when using SQLAlchemy text(), no eval needed
                vitals = row.vitals if isinstance(row.vitals, dict) else {}
                
                # Parse blood pressure string format "120/80" or dict format
                bp = vitals.get('blood_pressure')
                if isinstance(bp, str) and '/' in bp:
                    parts = bp.split('/')
                    bp_obj = {'systolic': int(parts[0]), 'diastolic': int(parts[1])}
                else:
                    bp_obj = bp
                
                vitals_data.append({
                    'patient_id': row.patient_id,
                    'vitals_measurement_date': row.vitals_measurement_date.strftime('%Y-%m-%d %H:%M:%S') if row.vitals_measurement_date else 'N/A',
                    'measurement_source': row.measurement_source or 'unknown',
                    'blood_pressure': bp_obj,
                    'pulse': vitals.get('pulse')
                })
            return vitals_data
    except Exception as e:
        print(f"Error fetching vitals: {e}")
        return []

def analyze_vitals(vitals_data):
    if not vitals_data:
        return "No vitals data found."
    
    vitals_text = "Vitals Data from Medical Records Database:\n\n"
    for record in vitals_data:
        date_str = record['vitals_measurement_date'] or 'N/A'
        source = record['measurement_source'] or 'unknown'
        vitals_text += f"Patient {record['patient_id']}:"
        vitals_text += f" Measurement: {date_str}, Source: {source}\n"
        bp = record['blood_pressure']
        pulse = record['pulse']
        bp_str = f"{bp['systolic']}/{bp['diastolic']} mmHg" if isinstance(bp, dict) else str(bp)
        pulse_str = str(pulse) if pulse is not None else 'None'
        vitals_text += f"BP: {bp_str}, Pulse: {pulse_str} bpm\n\n"
    
    prompt = """
Analyze these vital signs including measurement timestamps and provide:
1. Health assessment (BP/Pulse analysis)
2. Normal vs concerning ranges
3. Patient-by-patient interpretation with temporal awareness
4. Overall summary and recommendations
"""
    response = chat(model=MODEL, messages=[{"role": "user", "content": vitals_text + "\n" + prompt}])
    return response['message']['content']

def main(patient_id=None):
    print("="*70)
    print("VITAL SIGNS ANALYSIS")
    print("(" + (patient_id or "ALL PATIENTS") + ")")
    print("="*70)
    vitals_data = extract_vitals(patient_id)
    if not vitals_data:
        print("No vitals data found.")
        return
    print(f"Found {len(vitals_data)} patient(s) with vitals.")
    print("Analyzing with AI...")
    analysis = analyze_vitals(vitals_data)
    print("\n" + "="*70)
    print("AI ANALYSIS RESULT:")
    print(analysis)
    print("="*70)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        patient_id = sys.argv[1]
    else:
        patient_id = None
    main(patient_id)
