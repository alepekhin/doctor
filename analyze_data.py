"""Analyze medical records using Ollama model."""

import sys
from sqlalchemy import create_engine, text
from ollama import chat

from config import get_connection_uri, get_model


MODEL = get_model()


def fetch_medical_records(patient_id=None):
    """Fetch medical records from database."""
    engine = create_engine(get_connection_uri())
    with engine.connect() as conn:
        if patient_id:
            query = text(f"""
                SELECT id, patient_id, data, schema_info 
                FROM medical_data 
                WHERE patient_id = :patient_id
                ORDER BY id
            """)
            result = conn.execute(query, {"patient_id": patient_id})
        else:
            result = conn.execute(text("""
                SELECT id, patient_id, data, schema_info 
                FROM medical_data 
                ORDER BY id
            """))
        
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
    """Send records to carstenuhlig model for analysis."""
    records_text = """Extracted Medical Data Records:
    """
    for record in records:
        records_text += f"\n--- Record ID {record['id']} (Patient: {record['patient_id']}) ---\n"
        records_text += "Data fields: {" + ", ".join(record['data'].keys()) + "}\n"
        records_text += f"Schema: {record['schema_info']}\n"
    
    prompt = f"""
You are given a set of medical records stored in a PostgreSQL database using JSONB.

Here are the records:
{records_text}

Please analyze these records and provide:

1. **Schema Analysis**: What fields are consistently used across records?
2. **Data Patterns**: Are there common data structures or missing information?
3. **Recommendations**: What improvements could be made to the schema or data model?
4. **Potential Issues**: What constraints, validation, or data quality issues should be considered?

Be specific and actionable in your recommendations.
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

def main(patient_id=None):
    print(f"Connecting to database...")
    records = fetch_medical_records(patient_id)
    print(f"Found {len(records)} record(s).")
    
    if not records:
        print("No records found.")
        return
    
    print(f"\nAnalyzing with Ollama model: {MODEL}")
    print("="*60)
    
    analysis = analyze_with_ollama(records)
    
    print("="*60)
    print("\nANALYSIS RESULT:")
    print("-"*60)
    print(analysis)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        patient_id = sys.argv[1]
    else:
        patient_id = None
    main(patient_id)
