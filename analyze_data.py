"""Analyze medical records using Ollama model."""

from ollama import chat
from sqlalchemy import create_engine, text

# Database credentials
DB_URL = "postgresql://postgres:mysecretpassword@localhost/postgres"
MODEL = "carstenuhlig/omnicoder-2-9b:latest"

def fetch_medical_records():
    """Fetch medical records from database."""
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, patient_id, data, schema_info FROM medical_data ORDER BY id"))
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

def main():
    print(f"Connecting to {DB_URL}...")
    records = fetch_medical_records()
    print(f"Found {len(records)} records.")
    
    print(f"\nAnalyzing with Ollama model: {MODEL}")
    print("="*60)
    
    analysis = analyze_with_ollama(records)
    
    print("="*60)
    print("\nANALYSIS RESULT:\n")
    print("-"*60)
    print(analysis)

if __name__ == "__main__":
    main()
