"""Extract and analyze vitals data using Ollama AI."""

from sqlalchemy import create_engine, text
from ollama import chat

DB_URL = "postgresql://postgres:mysecretpassword@localhost/postgres"
MODEL = "carstenuhlig/omnicoder-2-9b:latest"

def extract_vitals():
    """Fetch blood pressure and pulse from medical_data table."""
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT patient_id, 
                   data->>'name' as name,
                   data->>'age' as age,
                   data->'vitals' as vitals
            FROM medical_data
            WHERE data ? 'vitals'
        """))
        
        vitals_data = []
        for row in result:
            v = row.vitals if hasattr(row, 'vitals') else row[2]
            vitals_data.append({
                'patient_id': row[0],
                'name': row[1],
                'age': row[2] if row[2] else None,
                'blood_pressure': v.get('blood_pressure') if v else None,
                'pulse': v.get('pulse') if v else None
            })
        return vitals_data

def analyze_vitals(vitals_data):
    vitals_text = "Vitals Data from Medical Records Database:\n\n"
    for record in vitals_data:
        vitals_text += f"Patient {record['patient_id']}: "
        vitals_text += f"{record['name']} (Age {record['age']})\n"
        vitals_text += f"  BP: {record['blood_pressure']}, Pulse: {record['pulse']} bpm\n"
    
    prompt = """
Analyze these vital signs and provide:
1. Health assessment (BP/Pulse analysis)
2. Normal vs concerning ranges
3. Patient-by-patient interpretation
4. Overall summary and recommendations
"""
    response = chat(model=MODEL, messages=[{"role": "user", "content": vitals_text + "\n" + prompt}])
    return response['message']['content']

def main():
    print("="*70 + "\nVITAL SIGNS ANALYSIS\n" + "="*70)
    vitals_data = extract_vitals()
    if not vitals_data:
        print("No vitals data found.")
        return
    print(f"Found {len(vitals_data)} patient(s) with vitals.")
    print("Analyzing with AI...")
    analysis = analyze_vitals(vitals_data)
    print("\n" + "="*70 + "\nAI ANALYSIS RESULT:\n")
    print(analysis)
    print("="*70)

if __name__ == "__main__":
    main()
