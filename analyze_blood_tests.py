"""Analyze blood test/labs data for specific patients using Ollama AI."""

import sys
from sqlalchemy import create_engine, text
from ollama import chat

from config import get_connection_uri, get_model


MODEL = get_model()


def fetch_blood_tests(patient_id=None):
    """Fetch blood test/labs data from database."""
    engine = create_engine(get_connection_uri())
    with engine.connect() as conn:
        if patient_id:
            query = text(f"""
                SELECT id, patient_id, data->'labs' as labs, 
                        data->'clinical_blood_tests' as clinical_tests,
                        vitals_measurement_date
                FROM medical_data
                WHERE patient_id = :patient_id
                  AND (data->'labs' IS NOT NULL OR data->'clinical_blood_tests' IS NOT NULL)
                ORDER BY vitals_measurement_date DESC NULLS LAST
            """)
            result = conn.execute(query, {"patient_id": patient_id})
        else:
            query = text("""
                SELECT id, patient_id, data->'labs' as labs, 
                        data->'clinical_blood_tests' as clinical_tests,
                        vitals_measurement_date
                FROM medical_data
                WHERE (data->'labs' IS NOT NULL OR data->'clinical_blood_tests' IS NOT NULL)
                ORDER BY patient_id, vitals_measurement_date DESC NULLS LAST
            """)
            result = conn.execute(query)
        
        tests = []
        for row in result:
            labs = row.labs if isinstance(row.labs, dict) and row.labs else {}
            clinical = row.clinical_tests if isinstance(row.clinical_tests, dict) and row.clinical_tests else {}
            
            tests.append({
                "id": row.id,
                "patient_id": row.patient_id,
                "labs": labs,
                "clinical_tests": clinical,
                "measurement_date": row.vitals_measurement_date.strftime('%Y-%m-%d %H:%M:%S') if row.vitals_measurement_date else 'N/A'
            })
        return tests


def analyze_blood_tests(tests, patient_id=None):
    """Send blood tests to carstenuhlig model for analysis."""
    if not tests and patient_id:
        return "No blood tests found for patient." + \
               "\n\nTo include all blood tests, run without --patient-id."
    
    tests_text = "Blood Test Data from Medical Records Database:\n\n"
    for test in tests:
        patient_ref = f"Patient {test['patient_id']}" if patient_id is None else f"{patient_id}"
        tests_text += f"{patient_ref} (ID: {test['id']}):"
        if test['measurement_date']:
            tests_text += f"  Date: {test['measurement_date']}"
        tests_text += "\n"
        
        labs = test['labs']
        if labs:
            tests_text += "  Labs:"
            for key, value in labs.items():
                tests_text += f"\n    - {key}: {value}"
        tests_text += "\n"
        
        clinical = test['clinical_tests']
        if clinical:
            tests_text += "  Clinical Tests:"
            for key, value in clinical.items():
                tests_text += f"\n    - {key}: {value}"
        tests_text += "\n\n"
    
    if tests and patient_id:
        prompt = f"""
Analyze these blood test results for patient analysis:

{tests_text}

Provide:
1. Complete results summary
2. Normal vs abnormal values analysis
3. Interpretations for each test
4. Overall health insights and recommendations
"""
    else:
        prompt = f"""
Analyze these blood test results across patients:

{tests_text}

Group by patient and provide:
1. Results summary per patient
2. Test-by-test analysis with normal ranges
3. Overall patterns and trends
4. Clinical interpretations and recommendations
"""
    
    response = chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return response['message']['content']


def main(patient_id=None):
    print("="*70)
    print("BLOOD TEST ANALYSIS")
    print((f"(ALL PATIENTS)" if patient_id is None else f"(PATIENT: {patient_id})"))
    print("="*70)
    
    tests = fetch_blood_tests(patient_id)
    if not tests:
        print("No blood tests found.")
        return
    
    print(f"Found {len(tests)} blood test(s)")
    print("Analyzing...")
    
    analysis = analyze_blood_tests(tests, patient_id)
    
    print("\n" + "="*70)
    print("ANALYSIS RESULT:")
    print(analysis)
    print("="*70)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        patient_id = sys.argv[1]
    else:
        patient_id = None
    main(patient_id)
