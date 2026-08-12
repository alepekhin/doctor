"""Analyze blood test records using Ollama AI."""

import sys
from sqlalchemy import create_engine, text
from ollama import chat

from config import get_connection_uri, get_model


MODEL = get_model()


def fetch_blood_test_records():
    """Fetch records with blood test data from database."""
    engine = create_engine(get_connection_uri())
    with engine.connect() as conn:
        query = text("SELECT id, patient_id, data, schema_info FROM medical_data WHERE data->'labs' IS NOT NULL ORDER BY id")
        result = conn.execute(query)
        
        records = []
        for row in result:
            records.append({
                "id": row.id,
                "patient_id": row.patient_id,
                "data": row.data,
                "schema_info": row.schema_info
            })
        return records


def analyze_with_ollama(records):
    """Send blood test records to AI for analysis."""
    records_text = ""
    for record in records:
        records_text += f"\n--- Record ID {record['id']} (Patient: {record['patient_id']}) ---\n"
        labs = record['data'].get('labs', {})
        records_text += f"Labs: {labs}\n"
        history = record['data'].get('history', {})
        records_text += f"Conditions: {history.get('conditions', 'None')}, Medications: {history.get('medications', 'None')}\n"
    
    prompt = f"""
    You are given a set of blood test records from a PostgreSQL database.

    Here are the records:
    {records_text}

    Please analyze these blood test results and provide:

    1. **Summary**: Identify key findings across all patients
    2. **Abnormal Values**: List elevated or low values with normal ranges
    3. **Risk Assessment**: Identify patients with multiple risk factors
    4. **Recommendations**: Clinical follow-up suggestions
    5. **Patterns**: Common conditions or trends across patients

    Be specific and actionable in your analysis.
    """
    
    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )
    
    return response['message']['content']


def main():
    print("Connecting to database...")
    records = fetch_blood_test_records()
    print(f"Found {len(records)} blood test record(s).")
    
    if not records:
        print("No blood test records found.")
        return
    
    print(f"\nAnalyzing with Ollama model: {MODEL}")
    print("="*60)
    
    analysis = analyze_with_ollama(records)
    
    print("="*60)
    print("\nBLOOD TEST ANALYSIS RESULT:")
    print("-"*60)
    print(analysis)


if __name__ == "__main__":
    main()
